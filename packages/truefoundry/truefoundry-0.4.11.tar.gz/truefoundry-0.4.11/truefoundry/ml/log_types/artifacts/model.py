import copy
import datetime
import json
import logging
import os.path
import tempfile
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Tuple, Union

from truefoundry.ml.artifact.truefoundry_artifact_repo import (
    ArtifactIdentifier,
    MlFoundryArtifactsRepository,
)
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    AddCustomMetricsToModelVersionRequestDto,
    ArtifactType,
    CreateArtifactVersionRequestDto,
    CreateModelVersionRequestDto,
    DeleteArtifactVersionsRequestDto,
    FinalizeArtifactVersionRequestDto,
    MetricDto,
    MlfoundryArtifactsApi,
    ModelDto,
    ModelVersionDto,
    NotifyArtifactVersionFailureDto,
    UpdateModelVersionRequestDto,
)
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    InternalMetadata as InternalMetadataDto,
)
from truefoundry.ml.enums import ModelFramework
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.log_types.artifacts.constants import (
    FILES_DIR,
    INTERNAL_METADATA_PATH,
    MODEL_DIR_NAME,
    MODEL_SCHEMA_UPDATE_FAILURE_HELP,
)
from truefoundry.ml.log_types.artifacts.model_extras import CustomMetric, ModelSchema
from truefoundry.ml.log_types.artifacts.utils import (
    _copy_additional_files,
    _get_src_dest_pairs,
    _validate_artifact_metadata,
    _validate_description,
    calculate_total_size,
)
from truefoundry.ml.session import _get_api_client
from truefoundry.pydantic_v1 import BaseModel, Extra
from truefoundry.version import __version__

if TYPE_CHECKING:
    from truefoundry.ml.mlfoundry_run import MlFoundryRun

logger = logging.getLogger(__name__)


# TODO: Support async download and upload


class ModelVersionInternalMetadata(BaseModel):
    class Config:
        extra = Extra.allow

    files_dir: str  # relative to root
    model_dir: str  # relative to `files_dir`
    model_is_null: bool = False
    framework: ModelFramework = ModelFramework.UNKNOWN
    transformers_pipeline_task: Optional[str] = None
    model_filename: Optional[str] = None
    mlfoundry_version: Optional[str] = None
    truefoundry_version: Optional[str] = None

    def dict(self, *args, **kwargs):
        dct = super().dict(*args, **kwargs)
        dct["framework"] = dct["framework"].value
        return dct


class ModelVersionDownloadInfo(BaseModel):
    download_dir: str
    model_dir: str
    model_framework: ModelFramework = ModelFramework.UNKNOWN
    model_filename: Optional[str] = None


class ModelVersion:
    def __init__(
        self,
        model_version: ModelVersionDto,
        model: ModelDto,
    ) -> None:
        self._api_client = _get_api_client()
        self._mlfoundry_artifacts_api = MlfoundryArtifactsApi(
            api_client=self._api_client
        )
        self._model_version = model_version
        self._model = model
        self._deleted = False
        self._description: str = ""
        self._metadata: Dict[str, Any] = {}
        self._metrics: List[MetricDto] = []
        self._set_metrics_attr()
        self._set_mutable_attrs()

    @classmethod
    def from_fqn(cls, fqn: str) -> "ModelVersion":
        """
        Get the version of a model to download contents or load them in memory

        Args:
            fqn (str): Fully qualified name of the model version.

        Returns:
            ModelVersion: An ModelVersion instance of the Model

        Examples:

            ```python
            from truefoundry.ml import get_client, ModelVersion

            client = get_client()
            model_version = ModelVersion.from_fqn(fqn="<your-model-fqn>")
            ```
        """
        api_client = _get_api_client()
        mlfoundry_artifacts_api = MlfoundryArtifactsApi(api_client=api_client)
        _model_version = mlfoundry_artifacts_api.get_model_version_by_fqn_get(fqn=fqn)
        model_version = _model_version.model_version
        _model = mlfoundry_artifacts_api.get_model_get(id=model_version.model_id)
        model = _model.model
        instance = cls(model_version=model_version, model=model)
        return instance

    def _ensure_not_deleted(self):
        if self._deleted:
            raise MlFoundryException(
                "Model Version was deleted, cannot perform updates on a deleted version"
            )

    def _set_metrics_attr(self):
        self._metrics = sorted(
            self._model_version.metrics or [], key=lambda m: m.timestamp
        )

    def _set_mutable_attrs(self):
        self._description = self._model_version.description or ""
        self._metadata = copy.deepcopy(self._model_version.artifact_metadata)

    def _refetch_model_version(self):
        _model_version = self._mlfoundry_artifacts_api.get_model_version_get(
            id=self._model_version.id
        )
        self._model_version = _model_version.model_version
        self._set_metrics_attr()
        self._set_mutable_attrs()

    def __repr__(self):
        return f"{self.__class__.__name__}(fqn={self.fqn!r})"

    def _get_artifacts_repo(self):
        return MlFoundryArtifactsRepository(
            artifact_identifier=ArtifactIdentifier(
                artifact_version_id=uuid.UUID(self._model_version.id)
            ),
            api_client=self._api_client,
        )

    @property
    def name(self) -> str:
        """Get the name of the model"""
        return self._model.name

    @property
    def model_fqn(self) -> str:
        """Get fqn of the model"""
        return self._model.fqn

    @property
    def version(self) -> int:
        """Get version information of the model"""
        return self._model_version.version

    @property
    def fqn(self) -> str:
        """Get fqn of the current model version"""
        return self._model_version.fqn

    @property
    def step(self) -> int:
        """Get the step in which model was created"""
        return self._model_version.step

    @property
    def description(self) -> Optional[str]:
        """Get description of the model"""
        return self._description

    @description.setter
    def description(self, value: str):
        """set the description of the model"""
        _validate_description(value)
        self._description = value

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata for the current model"""
        return self._metadata

    @metadata.setter
    def metadata(self, value: Dict[str, Any]):
        """set the metadata for current model"""
        _validate_artifact_metadata(value)
        self._metadata = value

    @property
    def metrics(self) -> Dict[str, Union[float, int]]:
        """get the metrics for the current version of the model"""
        metrics_as_kv: Dict[str, Union[float, int]] = {}
        for metric in self._metrics:
            metrics_as_kv[metric.key] = metric.value
        return metrics_as_kv

    @property
    def created_at(self) -> datetime.datetime:
        """Get the time at which model version was created"""
        return self._model_version.created_at

    @property
    def updated_at(self) -> datetime.datetime:
        """Get the information about when the model version was updated"""
        return self._model_version.updated_at

    def raw_download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> str:
        """
        Download a model file or directory to a local directory if applicable, and return a
        local path for it.

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified models. This directory must already exist.
                        If unspecified, the models will either be downloaded to a new
                        uniquely-named directory on the local filesystem.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            path:  Absolute path of the local filesystem location containing the desired models.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.raw_download(path="<your-desired-download-path>")
            ```
        """
        logger.info("Downloading model version contents, this might take a while ...")
        artifacts_repo = self._get_artifacts_repo()
        return artifacts_repo.download_artifacts(
            artifact_path="", dst_path=path, overwrite=overwrite, progress=progress
        )

    def _download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> Tuple[ModelVersionInternalMetadata, ModelVersionDownloadInfo]:
        self._ensure_not_deleted()
        download_dir = self.raw_download(
            path=path, overwrite=overwrite, progress=progress
        )
        internal_metadata_path = os.path.join(download_dir, INTERNAL_METADATA_PATH)
        if not os.path.exists(internal_metadata_path):
            raise MlFoundryException(
                "Model version seems to be corrupted or in invalid format due to missing model metadata. "
                "You can still use .raw_download(path='/your/path/here') to download and inspect files."
            )
        with open(internal_metadata_path) as f:
            internal_metadata = ModelVersionInternalMetadata.parse_obj(json.load(f))
        download_info = ModelVersionDownloadInfo(
            download_dir=os.path.join(download_dir, internal_metadata.files_dir),
            model_dir=os.path.join(
                download_dir, internal_metadata.files_dir, internal_metadata.model_dir
            ),
            model_framework=internal_metadata.framework,
            model_filename=internal_metadata.model_filename,
        )
        return internal_metadata, download_info

    def download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> ModelVersionDownloadInfo:
        """
        Download a model file or directory to a local directory if applicable, and return download info
        containing `model_dir` - local path where model was downloaded

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified models. This directory must already exist.
                        If unspecified, the models will either be downloaded to a new
                        uniquely-named directory on the local filesystem.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            ModelVersionDownloadInfo:  Download Info instance containing
                `model_dir` (path to downloaded model folder) and other metadata

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            download_info = model_version.download(path="<your-desired-download-path>")
            print(download_info.model_dir)
            ```
        """
        _, download_info = self._download(
            path=path, overwrite=overwrite, progress=progress
        )
        return download_info

    def delete(self) -> bool:
        """
        Deletes the current instance of the ModelVersion hence deleting the current version.

        Returns:
            True if model was deleted successfully

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.delete()
            ```
        """
        self._ensure_not_deleted()
        self._mlfoundry_artifacts_api.delete_artifact_version_post(
            delete_artifact_versions_request_dto=DeleteArtifactVersionsRequestDto(
                id=self._model_version.id
            )
        )
        self._deleted = True
        return True

    def update(self):
        """
        Updates the current instance of the ModelVersion hence updating the current version.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            model_version = client.get_model_version_by_fqn(fqn="<your-model-fqn>")
            model_version.description = 'This is the new description'
            model_version.update()
            ```
        """
        self._ensure_not_deleted()
        _model_version = self._mlfoundry_artifacts_api.update_model_version_post(
            update_model_version_request_dto=UpdateModelVersionRequestDto(
                id=self._model_version.id,
                description=self.description,
                artifact_metadata=self.metadata,
            )
        )
        self._model_version = _model_version.model_version
        self._set_metrics_attr()
        self._set_mutable_attrs()


def _log_model_version(  # noqa: C901
    run: Optional["MlFoundryRun"],
    name: str,
    model_file_or_folder: str,
    framework: Optional[Union[ModelFramework, str]],
    mlfoundry_artifacts_api: Optional[MlfoundryArtifactsApi] = None,
    ml_repo_id: Optional[str] = None,
    additional_files: Sequence[Tuple[Union[str, Path], Optional[str]]] = (),
    description: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    model_schema: Optional[Union[Dict[str, Any], ModelSchema]] = None,
    custom_metrics: Optional[List[Union[CustomMetric, Dict[str, Any]]]] = None,
    step: Optional[int] = 0,
    progress: Optional[bool] = None,
) -> ModelVersion:
    if (run and mlfoundry_artifacts_api) or (not run and not mlfoundry_artifacts_api):
        raise MlFoundryException(
            "Exactly one of run, mlfoundry_artifacts_api should be passed"
        )
    if mlfoundry_artifacts_api and not ml_repo_id:
        raise MlFoundryException(
            "If mlfoundry_artifacts_api is passed, ml_repo_id must also be passed"
        )
    if run:
        mlfoundry_artifacts_api = run._mlfoundry_artifacts_api

    assert mlfoundry_artifacts_api is not None

    custom_metrics = custom_metrics or []
    metadata = metadata or {}
    additional_files = additional_files or {}
    step = step or 0

    # validations
    if framework is None:
        framework = ModelFramework.UNKNOWN
    elif not isinstance(framework, ModelFramework):
        framework = ModelFramework(framework)

    _validate_description(description)
    _validate_artifact_metadata(metadata)

    if model_schema is not None and not isinstance(model_schema, ModelSchema):
        model_schema = ModelSchema.parse_obj(model_schema)

    if custom_metrics and not model_schema:
        raise MlFoundryException(
            "Custom Metrics defined without adding the Model Schema"
        )
    custom_metrics = [
        CustomMetric.parse_obj(cm) if not isinstance(cm, CustomMetric) else cm
        for cm in custom_metrics
    ]

    logger.info("Logging model and additional files, this might take a while ...")
    temp_dir = tempfile.TemporaryDirectory(prefix="truefoundry-")

    internal_metadata = ModelVersionInternalMetadata(
        framework=framework,
        files_dir=FILES_DIR,
        model_dir=MODEL_DIR_NAME,
        model_filename=(
            os.path.basename(model_file_or_folder)
            if model_file_or_folder and os.path.isfile(model_file_or_folder)
            else None
        ),
        mlfoundry_version=__version__,
        truefoundry_version=__version__,
    )

    try:
        local_files_dir = os.path.join(temp_dir.name, internal_metadata.files_dir)
        os.makedirs(local_files_dir, exist_ok=True)
        # in case model was None, we still create an empty dir
        local_model_dir = os.path.join(local_files_dir, internal_metadata.model_dir)
        os.makedirs(local_model_dir, exist_ok=True)

        logger.info("Adding model file/folder to model version content")
        _model_file_or_folder: Sequence[Tuple[str, str]] = [
            (model_file_or_folder, MODEL_DIR_NAME.rstrip(os.sep) + os.sep),
        ]

        temp_dest_to_src_map = _copy_additional_files(
            root_dir=temp_dir.name,
            files_dir=internal_metadata.files_dir,
            model_dir=internal_metadata.model_dir,
            additional_files=_model_file_or_folder,
            ignore_model_dir_dest_conflict=True,
        )

        # verify additional files and paths, copy additional files
        if additional_files:
            logger.info("Adding `additional_files` to model version contents")
            temp_dest_to_src_map = _copy_additional_files(
                root_dir=temp_dir.name,
                files_dir=internal_metadata.files_dir,
                model_dir=internal_metadata.model_dir,
                additional_files=additional_files,
                ignore_model_dir_dest_conflict=False,
                existing_dest_to_src_map=temp_dest_to_src_map,
            )
    except Exception as e:
        temp_dir.cleanup()
        raise MlFoundryException("Failed to log model") from e

    # save internal metadata
    local_internal_metadata_path = os.path.join(temp_dir.name, INTERNAL_METADATA_PATH)
    os.makedirs(os.path.dirname(local_internal_metadata_path), exist_ok=True)
    with open(local_internal_metadata_path, "w") as f:
        json.dump(internal_metadata.dict(), f)
    temp_dest_to_src_map[local_internal_metadata_path] = local_internal_metadata_path

    # create entry
    _create_artifact_version_response = (
        mlfoundry_artifacts_api.create_artifact_version_post(
            create_artifact_version_request_dto=CreateArtifactVersionRequestDto(
                experiment_id=int(run._experiment_id if run else ml_repo_id),
                artifact_type=ArtifactType.MODEL,
                name=name,
            )
        )
    )
    version_id = _create_artifact_version_response.id
    artifacts_repo = MlFoundryArtifactsRepository(
        artifact_identifier=ArtifactIdentifier(
            artifact_version_id=uuid.UUID(version_id)
        ),
        api_client=mlfoundry_artifacts_api.api_client,
    )

    total_size = calculate_total_size(list(temp_dest_to_src_map.values()))
    try:
        logger.info(
            "Packaging and uploading files to remote with size: %.6f MB",
            total_size / 1000000.0,
        )
        src_dest_pairs = _get_src_dest_pairs(
            root_dir=temp_dir.name, dest_to_src_map=temp_dest_to_src_map
        )
        artifacts_repo.log_artifacts(src_dest_pairs=src_dest_pairs, progress=progress)
    except Exception as e:
        mlfoundry_artifacts_api.notify_failure_post(
            notify_artifact_version_failure_dto=NotifyArtifactVersionFailureDto(
                id=version_id
            )
        )
        raise MlFoundryException("Failed to log model") from e
    finally:
        temp_dir.cleanup()

    # Note: Here we call from_dict instead of directly passing in init and relying on it
    # to convert because the complicated union of types generates a custom type to handle casting
    # Check the source of `InternalMetadataDto` to see the generated code
    internal_metadata_dto = InternalMetadataDto.from_dict(
        internal_metadata.dict() if internal_metadata is not None else {}
    )
    mlfoundry_artifacts_api.finalize_artifact_version_post(
        finalize_artifact_version_request_dto=FinalizeArtifactVersionRequestDto(
            id=version_id,
            run_uuid=run.run_id if run else None,
            artifact_size=total_size,
            internal_metadata=internal_metadata_dto,
            step=step if run else None,
        )
    )
    _model_version = mlfoundry_artifacts_api.create_model_version_post(
        create_model_version_request_dto=CreateModelVersionRequestDto(
            artifact_version_id=version_id,
            description=description,
            artifact_metadata=metadata,
            internal_metadata=internal_metadata_dto,
            data_path=INTERNAL_METADATA_PATH,
            step=step if run else None,
        )
    )
    model_version = _model_version.model_version

    # update model schema at end
    update_args: Dict[str, Any] = {
        "id": version_id,
        "model_framework": framework.value,
    }
    if model_schema:
        update_args["model_schema"] = model_schema

    try:
        _model_version = mlfoundry_artifacts_api.update_model_version_post(
            update_model_version_request_dto=UpdateModelVersionRequestDto(**update_args)
        )
        model_version = _model_version.model_version
        if model_schema:
            _model_version = mlfoundry_artifacts_api.add_custom_metrics_to_model_version_post(
                add_custom_metrics_to_model_version_request_dto=AddCustomMetricsToModelVersionRequestDto(
                    id=version_id, custom_metrics=custom_metrics
                )
            )
            model_version = _model_version.model_version
    except Exception:
        # TODO (chiragjn): what is the best exception to catch here?
        logger.error(MODEL_SCHEMA_UPDATE_FAILURE_HELP.format(fqn=model_version.fqn))

    return ModelVersion.from_fqn(fqn=model_version.fqn)
