import copy
import datetime
import json
import os
import tempfile
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, NamedTuple, Optional, Tuple, Union

from truefoundry.ml.artifact.truefoundry_artifact_repo import (
    ArtifactIdentifier,
    MlFoundryArtifactsRepository,
)
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ArtifactDto,
    ArtifactType,
    ArtifactVersionDto,
    CreateArtifactVersionRequestDto,
    DeleteArtifactVersionsRequestDto,
    FinalizeArtifactVersionRequestDto,
    MlfoundryArtifactsApi,
    NotifyArtifactVersionFailureDto,
    UpdateArtifactVersionRequestDto,
)
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    InternalMetadata as InternalMetadataDto,
)
from truefoundry.ml.autogen.entities.artifacts import ChatPrompt
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.log_types.artifacts.constants import INTERNAL_METADATA_PATH
from truefoundry.ml.log_types.artifacts.utils import (
    _get_src_dest_pairs,
    _validate_artifact_metadata,
    _validate_description,
    calculate_total_size,
)
from truefoundry.ml.logger import logger
from truefoundry.ml.session import _get_api_client
from truefoundry.pydantic_v1 import BaseModel, Extra

if TYPE_CHECKING:
    from truefoundry.ml.mlfoundry_run import MlFoundryRun


class ArtifactPath(NamedTuple):
    src: str
    dest: Optional[str] = None


class ArtifactVersionInternalMetadata(BaseModel):
    class Config:
        extra = Extra.allow

    files_dir: str  # relative to root


class ArtifactVersionDownloadInfo(BaseModel):
    download_dir: str
    content_dir: str


class ArtifactVersion:
    def __init__(
        self,
        artifact_version: ArtifactVersionDto,
        artifact: ArtifactDto,
    ) -> None:
        self._api_client = _get_api_client()
        self._mlfoundry_artifacts_api = MlfoundryArtifactsApi(
            api_client=self._api_client
        )
        self._artifact_version: ArtifactVersionDto = artifact_version
        self._artifact: ArtifactDto = artifact
        self._deleted = False
        self._description: str = ""
        self._metadata: Dict[str, Any] = {}
        self._set_mutable_attrs()

    @classmethod
    def from_fqn(cls, fqn: str) -> "ArtifactVersion":
        """
        Get the version of an Artifact to download contents or load them in memory

        Args:
            fqn (str): Fully qualified name of the artifact version.

        Returns:
            ArtifactVersion: An ArtifactVersion instance of the artifact

        Examples:

            ```python
            from truefoundry.ml import get_client, ArtifactVersion

            client = get_client()
            artifact_version = ArtifactVersion.from_fqn(fqn="<artifact-fqn>")
            ```
        """
        api_client = _get_api_client()
        mlfoundry_artifacts_api = MlfoundryArtifactsApi(api_client=api_client)
        _artifact_version = mlfoundry_artifacts_api.get_artifact_version_by_fqn_get(
            fqn=fqn
        )
        artifact_version = _artifact_version.artifact_version
        _artifact = mlfoundry_artifacts_api.get_artifact_by_id_get(
            id=artifact_version.artifact_id
        )
        return cls(
            artifact_version=_artifact_version.artifact_version,
            artifact=_artifact.artifact,
        )

    def _ensure_not_deleted(self):
        if self._deleted:
            raise MlFoundryException(
                "Artifact Version was deleted, cannot access a deleted version"
            )

    def _set_mutable_attrs(self, refetch=False):
        if refetch:
            _artifact_version = (
                self._mlfoundry_artifacts_api.get_artifact_version_by_id_get(
                    id=self._artifact_version.id
                )
            )
            self._artifact_version = _artifact_version.artifact_version
        self._description = self._artifact_version.description or ""
        self._metadata = copy.deepcopy(self._artifact_version.artifact_metadata)

    def __repr__(self):
        return f"{self.__class__.__name__}(fqn={self.fqn!r})"

    def _get_artifacts_repo(self):
        return MlFoundryArtifactsRepository(
            artifact_identifier=ArtifactIdentifier(
                artifact_version_id=uuid.UUID(self._artifact_version.id)
            ),
            api_client=self._api_client,
        )

    @property
    def name(self) -> str:
        """Get the name of the artifact"""
        return self._artifact.name

    @property
    def artifact_fqn(self) -> str:
        """Get fqn of the artifact"""
        return self._artifact.fqn

    @property
    def version(self) -> int:
        """Get version information of the artifact"""
        return self._artifact_version.version

    @property
    def fqn(self) -> str:
        """Get fqn of the current artifact version"""
        return self._artifact_version.fqn

    @property
    def step(self) -> int:
        """Get the step in which artifact was created"""
        return self._artifact_version.step

    @property
    def description(self) -> Optional[str]:
        """Get description of the artifact"""
        return self._description

    @description.setter
    def description(self, value: str):
        """set the description of the artifact"""
        _validate_description(value)
        self._description = value

    @property
    def metadata(self) -> Dict[str, Any]:
        """Get metadata for the current artifact"""
        return self._metadata

    @metadata.setter
    def metadata(self, value: Dict[str, Any]):
        """set the metadata for current artifact"""
        _validate_artifact_metadata(value)
        self._metadata = value

    @property
    def created_at(self) -> datetime.datetime:
        """Get the time at which artifact was created"""
        return self._artifact_version.created_at

    @property
    def updated_at(self) -> datetime.datetime:
        """Get the information about when the artifact was updated"""
        return self._artifact_version.updated_at

    def raw_download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> str:
        """
        Download an artifact file or directory to a local directory if applicable, and return a
        local path for it.

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified artifacts. This directory must already exist.
                        If unspecified, the artifacts will either be downloaded to a new
                        uniquely-named directory on the local filesystem.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            path:  Absolute path of the local filesystem location containing the desired artifacts.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            artifact_version = client.get_artifact_version_by_fqn(fqn="<your-artifact-fqn>")
            artifact_version.raw_download(path="<your-desired-download-path>")
            ```
        """
        logger.info(
            "Downloading artifact version contents, this might take a while ..."
        )
        artifacts_repo = self._get_artifacts_repo()
        return artifacts_repo.download_artifacts(
            artifact_path="", dst_path=path, overwrite=overwrite, progress=progress
        )

    def _download(
        self,
        path: Optional[Union[str, Path]],
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> Tuple[ArtifactVersionInternalMetadata, str]:
        self._ensure_not_deleted()
        download_dir = self.raw_download(
            path=path, overwrite=overwrite, progress=progress
        )
        internal_metadata_path = os.path.join(download_dir, INTERNAL_METADATA_PATH)
        if not os.path.exists(internal_metadata_path):
            raise MlFoundryException(
                "Artifact version seems to be corrupted or in invalid format due to missing artifact metadata. "
                "You can still use .raw_download(path='/your/path/here') to download and inspect files."
            )
        with open(internal_metadata_path) as f:
            internal_metadata = ArtifactVersionInternalMetadata.parse_obj(json.load(f))
        download_path = os.path.join(download_dir, internal_metadata.files_dir)
        return internal_metadata, download_path

    def download(
        self,
        path: Optional[Union[str, Path]] = None,
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> str:
        """
        Download an artifact file or directory to a local directory if applicable, and return a
        local path for it.

        Args:
            path (str): Absolute path of the local filesystem destination directory to which to
                        download the specified artifacts. This directory must already exist.
                        If unspecified, the artifacts will either be downloaded to a new
                        uniquely-named directory on the local filesystem or will be returned
                        directly in the case of the Local ArtifactRepository.
            overwrite (bool): If True it will overwrite the file if it is already present in the download directory else
                              it will throw an error
            progress (bool): value to show progress bar, defaults to None.

        Returns:
            path:  Absolute path of the local filesystem location containing the desired artifacts.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            artifact_version = client.get_artifact_version_by_fqn(fqn="<your-artifact-fqn>")
            artifact_version.download(path="<your-desired-download-path>")
            ```
        """
        _, download_path = self._download(
            path=path, overwrite=overwrite, progress=progress
        )
        return download_path

    def delete(self) -> bool:
        """
        Deletes the current instance of the ArtifactVersion hence deleting the current version.

        Returns:
            True if artifact was deleted successfully

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            artifact_version = client.get_artifact_version_by_fqn(fqn="<your-artifact-fqn>")
            artifact_version.delete()
            ```
        """
        self._ensure_not_deleted()
        self._mlfoundry_artifacts_api.delete_artifact_version_post(
            delete_artifact_versions_request_dto=DeleteArtifactVersionsRequestDto(
                id=self._artifact_version.id
            )
        )
        self._deleted = True
        return True

    def update(self):
        """
        Updates the current instance of the ArtifactVersion hence updating the current version.

        Examples:

            ```python
            from truefoundry.ml import get_client

            client = get_client()
            artifact_version = client.get_artifact_version_by_fqn(fqn="<your-artifact-fqn>")
            artifact_version.description = 'This is the new description'
            artifact_version.update()
            ```
        """
        self._ensure_not_deleted()

        _artifact_version = self._mlfoundry_artifacts_api.update_artifact_version_post(
            update_artifact_version_request_dto=UpdateArtifactVersionRequestDto(
                id=self._artifact_version.id,
                description=self.description,
                artifact_metadata=self.metadata,
            )
        )
        self._artifact_version = _artifact_version.artifact_version
        self._set_mutable_attrs()


class ChatPromptVersion(ArtifactVersion):
    def __init__(self, artifact_version: ArtifactVersionDto, artifact: ArtifactDto):
        if artifact.type != ArtifactType.CHAT_PROMPT:
            raise ValueError(
                f"{artifact_version.fqn!r} is not a chat prompt type artifact"
            )
        super().__init__(
            artifact_version=artifact_version,
            artifact=artifact,
        )
        self._chat_prompt = ChatPrompt.parse_obj(
            artifact_version.internal_metadata.to_dict()
        )

    @classmethod
    def from_fqn(cls, fqn: str) -> "ChatPromptVersion":
        api_client = _get_api_client()
        mlfoundry_artifacts_api = MlfoundryArtifactsApi(api_client=api_client)
        _artifact_version = mlfoundry_artifacts_api.get_artifact_version_by_fqn_get(
            fqn=fqn
        )
        artifact_version = _artifact_version.artifact_version
        _artifact = mlfoundry_artifacts_api.get_artifact_by_id_get(
            id=artifact_version.artifact_id
        )
        return cls(
            artifact_version=_artifact_version.artifact_version,
            artifact=_artifact.artifact,
        )

    @property
    def model(self) -> str:
        return self._chat_prompt.model_configuration.model

    @property
    def provider(self) -> str:
        return self._chat_prompt.model_configuration.provider

    @property
    def messages(self) -> List[Dict[str, Any]]:
        return [message.dict() for message in self._chat_prompt.messages]

    @property
    def parameters(self) -> Dict[str, Any]:
        _parameters = self._chat_prompt.model_configuration.parameters
        return _parameters.dict(exclude_unset=True) if _parameters else {}

    @property
    def extra_parameters(self) -> Dict[str, Any]:
        _extra_parameters = self._chat_prompt.model_configuration.extra_parameters
        return _extra_parameters if _extra_parameters else {}

    @property
    def variables(self) -> Dict[str, Any]:
        return self._chat_prompt.variables or {}


def _log_artifact_version_helper(
    run: "MlFoundryRun",
    name: str,
    artifact_type: ArtifactType,
    artifact_dir: tempfile.TemporaryDirectory,
    dest_to_src_map: Dict[str, str],
    mlfoundry_artifacts_api: Optional[MlfoundryArtifactsApi] = None,
    ml_repo_id: Optional[str] = None,
    description: Optional[str] = None,
    internal_metadata: Optional[BaseModel] = None,
    metadata: Optional[Dict[str, Any]] = None,
    step: int = 0,
    progress: Optional[bool] = None,
) -> ArtifactVersion:
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
    _create_artifact_response = mlfoundry_artifacts_api.create_artifact_version_post(
        create_artifact_version_request_dto=CreateArtifactVersionRequestDto(
            experiment_id=int(run._experiment_id if run else ml_repo_id),
            name=name,
            artifact_type=artifact_type,
        )
    )
    version_id = _create_artifact_response.id
    artifacts_repo = MlFoundryArtifactsRepository(
        artifact_identifier=ArtifactIdentifier(
            artifact_version_id=uuid.UUID(version_id),
        ),
        api_client=mlfoundry_artifacts_api.api_client,
    )

    total_size = calculate_total_size(list(dest_to_src_map.values()))
    try:
        logger.info(
            "Packaging and uploading files to remote with size: %.6f MB",
            total_size / 1000000.0,
        )
        src_dest_pairs = _get_src_dest_pairs(
            root_dir=artifact_dir.name, dest_to_src_map=dest_to_src_map
        )
        artifacts_repo.log_artifacts(src_dest_pairs=src_dest_pairs, progress=progress)
    except Exception as e:
        mlfoundry_artifacts_api.notify_failure_post(
            notify_artifact_version_failure_dto=NotifyArtifactVersionFailureDto(
                id=version_id
            )
        )
        raise MlFoundryException("Failed to log Artifact") from e
    finally:
        artifact_dir.cleanup()

    # Note: Here we call from_dict instead of directly passing in init and relying on it
    # to convert because the complicated union of types generates a custom type to handle casting
    # Check the source of `InternalMetadataDto` to see the generated code
    internal_metadata_dto = InternalMetadataDto.from_dict(
        internal_metadata.dict() if internal_metadata is not None else {}
    )
    finalize_artifact_version_request_dto = FinalizeArtifactVersionRequestDto(
        id=version_id,
        run_uuid=run.run_id if run else None,
        description=description,
        internal_metadata=internal_metadata_dto,
        artifact_metadata=metadata,
        data_path=INTERNAL_METADATA_PATH,
        step=step,
        artifact_size=total_size,
    )
    _artifact_version = mlfoundry_artifacts_api.finalize_artifact_version_post(
        finalize_artifact_version_request_dto=finalize_artifact_version_request_dto
    )
    return ArtifactVersion.from_fqn(fqn=_artifact_version.artifact_version.fqn)
