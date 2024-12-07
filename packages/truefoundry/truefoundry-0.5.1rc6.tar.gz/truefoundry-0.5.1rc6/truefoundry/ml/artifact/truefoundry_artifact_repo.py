import math
import mmap
import os
import posixpath
import sys
import tempfile
import uuid
from concurrent.futures import FIRST_EXCEPTION, Future, ThreadPoolExecutor, wait
from shutil import rmtree
from threading import Event
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Tuple,
    Union,
)
from urllib.parse import unquote
from urllib.request import pathname2url

import requests
from rich.console import _is_jupyter
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from tqdm.utils import CallbackIOWrapper

from truefoundry.common.constants import ENV_VARS
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ApiClient,
    CreateMultiPartUploadForDatasetRequestDto,
    CreateMultiPartUploadRequestDto,
    FileInfoDto,
    GetSignedURLForDatasetWriteRequestDto,
    GetSignedURLsForArtifactVersionReadRequestDto,
    GetSignedURLsForArtifactVersionWriteRequestDto,
    GetSignedURLsForDatasetReadRequestDto,
    ListFilesForArtifactVersionRequestDto,
    ListFilesForArtifactVersionsResponseDto,
    ListFilesForDatasetRequestDto,
    ListFilesForDatasetResponseDto,
    MlfoundryArtifactsApi,
    MultiPartUploadDto,
    MultiPartUploadResponseDto,
    MultiPartUploadStorageProvider,
    RunArtifactsApi,
    SignedURLDto,
)
from truefoundry.ml.clients.utils import (
    augmented_raise_for_status,
    cloud_storage_http_request,
)
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.logger import logger
from truefoundry.ml.session import _get_api_client
from truefoundry.pydantic_v1 import BaseModel, root_validator

_MIN_BYTES_REQUIRED_FOR_MULTIPART = 100 * 1024 * 1024
# GCP/S3 Maximum number of parts per upload	10,000
# Maximum number of blocks in a block blob 50,000 blocks
# TODO: This number is artificially limited now. Later
# we will ask for parts signed URI in batches rather than in a single
# API Calls:
# Create Multipart Upload (Returns maximum number of parts, size limit of
#                            a single part, upload id for s3 etc )
#   Get me signed uris for first 500 parts
#     Upload 500 parts
#   Get me signed uris for the next 500 parts
#     Upload 500 parts
#   ...
# Finalize the Multipart upload using the finalize signed url returned
# by Create Multipart Upload or get a new one.
_MAX_NUM_PARTS_FOR_MULTIPART = 1000
# Azure Maximum size of a block in a block blob	4000 MiB
# GCP/S3 Maximum size of an individual part in a multipart upload 5 GiB
_MAX_PART_SIZE_BYTES_FOR_MULTIPART = 4 * 1024 * 1024 * 1000
_LIST_FILES_PAGE_SIZE = 500
_GENERATE_SIGNED_URL_BATCH_SIZE = 50
DEFAULT_PRESIGNED_URL_EXPIRY_TIME = 3600


def _can_display_progress(user_choice: Optional[bool] = None) -> bool:
    if user_choice is False:
        return False

    if sys.stdout.isatty():
        return True
    elif _is_jupyter():
        try:
            from IPython.display import display  # noqa: F401
            from ipywidgets import Output  # noqa: F401

            return True
        except ImportError:
            logger.warning(
                "Detected Jupyter Environment. Install `ipywidgets` to display live progress bars.",
            )
    if user_choice is True:
        logger.warning(
            "`progress` argument is set to True but did not detect tty "
            "or jupyter environment with ipywidgets installed. "
            "Progress bars may not be displayed. "
        )
        return True
    return False


def relative_path_to_artifact_path(path):
    if os.path == posixpath:
        return path
    if os.path.abspath(path) == path:
        raise Exception("This method only works with relative paths.")
    return unquote(pathname2url(path))


def _align_part_size_with_mmap_allocation_granularity(part_size: int) -> int:
    modulo = part_size % mmap.ALLOCATIONGRANULARITY
    if modulo == 0:
        return part_size

    part_size += mmap.ALLOCATIONGRANULARITY - modulo
    return part_size


# Can not be less than 5 * 1024 * 1024
_PART_SIZE_BYTES_FOR_MULTIPART = _align_part_size_with_mmap_allocation_granularity(
    10 * 1024 * 1024
)


def bad_path_message(name):
    return (
        "Names may be treated as files in certain cases, and must not resolve to other names"
        " when treated as such. This name would resolve to '%s'"
    ) % posixpath.normpath(name)


def path_not_unique(name):
    norm = posixpath.normpath(name)
    return norm != name or norm == "." or norm.startswith("..") or norm.startswith("/")


def verify_artifact_path(artifact_path):
    if artifact_path and path_not_unique(artifact_path):
        raise MlFoundryException(
            f"Invalid artifact path: {artifact_path!r}. {bad_path_message(artifact_path)!r}"
        )


class _PartNumberEtag(NamedTuple):
    part_number: int
    etag: str


def _get_s3_compatible_completion_body(multi_parts: List[_PartNumberEtag]) -> str:
    body = "<CompleteMultipartUpload>\n"
    for part in multi_parts:
        body += "  <Part>\n"
        body += f"    <PartNumber>{part.part_number}</PartNumber>\n"
        body += f"    <ETag>{part.etag}</ETag>\n"
        body += "  </Part>\n"
    body += "</CompleteMultipartUpload>"
    return body


def _get_azure_blob_completion_body(block_ids: List[str]) -> str:
    body = "<BlockList>\n"
    for block_id in block_ids:
        body += f"<Uncommitted>{block_id}</Uncommitted> "
    body += "</BlockList>"
    return body


class _FileMultiPartInfo(NamedTuple):
    num_parts: int
    part_size: int
    file_size: int


def _decide_file_parts(file_path: str) -> _FileMultiPartInfo:
    file_size = os.path.getsize(file_path)
    if (
        file_size < _MIN_BYTES_REQUIRED_FOR_MULTIPART
        or ENV_VARS.TFY_ARTIFACTS_DISABLE_MULTIPART_UPLOAD
    ):
        return _FileMultiPartInfo(1, part_size=file_size, file_size=file_size)

    ideal_num_parts = math.ceil(file_size / _PART_SIZE_BYTES_FOR_MULTIPART)
    if ideal_num_parts <= _MAX_NUM_PARTS_FOR_MULTIPART:
        return _FileMultiPartInfo(
            ideal_num_parts,
            part_size=_PART_SIZE_BYTES_FOR_MULTIPART,
            file_size=file_size,
        )

    part_size_when_using_max_parts = math.ceil(file_size / _MAX_NUM_PARTS_FOR_MULTIPART)
    part_size_when_using_max_parts = _align_part_size_with_mmap_allocation_granularity(
        part_size_when_using_max_parts
    )
    if part_size_when_using_max_parts > _MAX_PART_SIZE_BYTES_FOR_MULTIPART:
        raise ValueError(
            f"file {file_path!r} is too big for upload. Multipart chunk"
            f" size {part_size_when_using_max_parts} is higher"
            f" than {_MAX_PART_SIZE_BYTES_FOR_MULTIPART}"
        )
    num_parts = math.ceil(file_size / part_size_when_using_max_parts)
    return _FileMultiPartInfo(
        num_parts, part_size=part_size_when_using_max_parts, file_size=file_size
    )


def _signed_url_upload_file(
    signed_url: SignedURLDto,
    local_file: str,
    progress_bar: Progress,
    abort_event: Optional[Event] = None,
):
    if os.stat(local_file).st_size == 0:
        with cloud_storage_http_request(
            method="put", url=signed_url.signed_url, data=""
        ) as response:
            augmented_raise_for_status(response)
        return

    task_progress_bar = progress_bar.add_task(
        f"[green]Uploading {local_file}:", start=True
    )

    def callback(length):
        progress_bar.update(
            task_progress_bar, advance=length, total=os.stat(local_file).st_size
        )
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(local_file, "rb") as file:
        # NOTE: Azure Put Blob does not support Transfer Encoding header.
        wrapped_file = CallbackIOWrapper(callback, file, "read")
        with cloud_storage_http_request(
            method="put", url=signed_url.signed_url, data=wrapped_file
        ) as response:
            augmented_raise_for_status(response)


def _download_file_using_http_uri(
    http_uri,
    download_path,
    chunk_size=ENV_VARS.TFY_ARTIFACTS_DOWNLOAD_CHUNK_SIZE_BYTES,
    callback: Optional[Callable[[int, int], Any]] = None,
):
    """
    Downloads a file specified using the `http_uri` to a local `download_path`. This function
    uses a `chunk_size` to ensure an OOM error is not raised a large file is downloaded.
    Note : This function is meant to download files using presigned urls from various cloud
            providers.
    """
    with cloud_storage_http_request(
        method="get", url=http_uri, stream=True
    ) as response:
        augmented_raise_for_status(response)
        file_size = int(response.headers.get("Content-Length", 0))
        with open(download_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if callback:
                    callback(len(chunk), file_size)
                if not chunk:
                    break
                output_file.write(chunk)
                if ENV_VARS.TFY_ARTIFACTS_DOWNLOAD_FSYNC_CHUNKS:
                    output_file.flush()
                    os.fsync(output_file.fileno())


class _CallbackIOWrapperForMultiPartUpload(CallbackIOWrapper):
    def __init__(self, callback, stream, method, length: int):
        self.wrapper_setattr("_length", length)
        super().__init__(callback, stream, method)

    def __len__(self):
        return self.wrapper_getattr("_length")


def _file_part_upload(
    url: str,
    file_path: str,
    seek: int,
    length: int,
    file_size: int,
    abort_event: Optional[Event] = None,
    method: str = "put",
):
    def callback(*_, **__):
        if abort_event and abort_event.is_set():
            raise Exception("aborting upload")

    with open(file_path, "rb") as file:
        with mmap.mmap(
            file.fileno(),
            length=min(file_size - seek, length),
            offset=seek,
            access=mmap.ACCESS_READ,
        ) as mapped_file:
            wrapped_file = _CallbackIOWrapperForMultiPartUpload(
                callback, mapped_file, "read", len(mapped_file)
            )
            with cloud_storage_http_request(
                method=method,
                url=url,
                data=wrapped_file,
            ) as response:
                augmented_raise_for_status(response)
                return response


def _s3_compatible_multipart_upload(
    multipart_upload: MultiPartUploadDto,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    progress_bar: Progress,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()
    parts = []

    multi_part_upload_progress = progress_bar.add_task(
        f"[green]Uploading {local_file}:", start=True
    )

    def upload(part_number: int, seek: int) -> None:
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        response = _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].signed_url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        progress_bar.update(
            multi_part_upload_progress,
            advance=multipart_info.part_size,
            total=multipart_info.file_size,
        )
        etag = response.headers["ETag"]
        parts.append(_PartNumberEtag(etag=etag, part_number=part_number + 1))

    futures: List[Future] = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    parts = sorted(parts, key=lambda part: part.part_number)
    response = requests.post(
        multipart_upload.finalize_signed_url.signed_url,
        data=_get_s3_compatible_completion_body(parts),
        timeout=2 * 60,
    )
    response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


def _azure_multi_part_upload(
    multipart_upload: MultiPartUploadDto,
    local_file: str,
    multipart_info: _FileMultiPartInfo,
    executor: ThreadPoolExecutor,
    progress_bar: Progress,
    abort_event: Optional[Event] = None,
):
    abort_event = abort_event or Event()

    multi_part_upload_progress = progress_bar.add_task(
        f"[green]Uploading {local_file}:", start=True
    )

    def upload(part_number: int, seek: int):
        logger.debug(
            "Uploading part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )
        _file_part_upload(
            url=multipart_upload.part_signed_urls[part_number].signed_url,
            file_path=local_file,
            seek=seek,
            length=multipart_info.part_size,
            file_size=multipart_info.file_size,
            abort_event=abort_event,
        )
        progress_bar.update(
            multi_part_upload_progress,
            advance=multipart_info.part_size,
            total=multipart_info.file_size,
        )
        logger.debug(
            "Uploaded part %d/%d of %s",
            part_number,
            multipart_info.num_parts,
            local_file,
        )

    futures: List[Future] = []
    for part_number, seek in enumerate(
        range(0, multipart_info.file_size, multipart_info.part_size)
    ):
        future = executor.submit(upload, part_number=part_number, seek=seek)
        futures.append(future)

    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
    if len(not_done) > 0:
        abort_event.set()
    for future in not_done:
        future.cancel()
    for future in done:
        if future.exception() is not None:
            raise future.exception()

    logger.debug("Finalizing multipart upload of %s", local_file)
    if multipart_upload.azure_blob_block_ids:
        response = requests.put(
            multipart_upload.finalize_signed_url.signed_url,
            data=_get_azure_blob_completion_body(
                block_ids=multipart_upload.azure_blob_block_ids
            ),
            timeout=2 * 60,
        )
        response.raise_for_status()
    logger.debug("Multipart upload of %s completed", local_file)


def _any_future_has_failed(futures) -> bool:
    return any(
        future.done() and not future.cancelled() and future.exception() is not None
        for future in futures
    )


class ArtifactIdentifier(BaseModel):
    artifact_version_id: Optional[uuid.UUID] = None
    dataset_fqn: Optional[str] = None

    @root_validator
    def _check_identifier_type(cls, values: Dict[str, Any]):
        if not values.get("artifact_version_id", False) and not values.get(
            "dataset_fqn", False
        ):
            raise MlFoundryException(
                "One of the version_id or dataset_fqn should be passed"
            )
        if values.get("artifact_version_id", False) and values.get(
            "dataset_fqn", False
        ):
            raise MlFoundryException(
                "Exactly one of version_id or dataset_fqn should be passed"
            )
        return values


class MlFoundryArtifactsRepository:
    def __init__(
        self,
        artifact_identifier: ArtifactIdentifier,
        api_client: Optional[ApiClient] = None,
    ):
        self.artifact_identifier = artifact_identifier
        self._api_client = api_client or _get_api_client()
        self._run_artifacts_api = RunArtifactsApi(api_client=self._api_client)
        self._mlfoundry_artifacts_api = MlfoundryArtifactsApi(
            api_client=self._api_client
        )

    # TODO (chiragjn): Refactor these methods - if else is very inconvenient
    def get_signed_urls_for_read(
        self,
        artifact_identifier: ArtifactIdentifier,
        paths,
    ) -> List[SignedURLDto]:
        if artifact_identifier.artifact_version_id:
            signed_urls_response = self._mlfoundry_artifacts_api.get_signed_urls_for_read_post(
                get_signed_urls_for_artifact_version_read_request_dto=GetSignedURLsForArtifactVersionReadRequestDto(
                    id=str(artifact_identifier.artifact_version_id), paths=paths
                )
            )
            signed_urls = signed_urls_response.signed_urls
        elif artifact_identifier.dataset_fqn:
            signed_urls_dataset_response = self._mlfoundry_artifacts_api.get_signed_urls_dataset_read_post(
                get_signed_urls_for_dataset_read_request_dto=GetSignedURLsForDatasetReadRequestDto(
                    dataset_fqn=artifact_identifier.dataset_fqn, paths=paths
                )
            )
            signed_urls = signed_urls_dataset_response.signed_urls
        else:
            raise ValueError(
                "Invalid artifact type - both `artifact_version_id` and `dataset_fqn` both are None"
            )
        return signed_urls

    def get_signed_urls_for_write(
        self,
        artifact_identifier: ArtifactIdentifier,
        paths: List[str],
    ) -> List[SignedURLDto]:
        if artifact_identifier.artifact_version_id:
            signed_urls_response = self._mlfoundry_artifacts_api.get_signed_urls_for_write_post(
                get_signed_urls_for_artifact_version_write_request_dto=GetSignedURLsForArtifactVersionWriteRequestDto(
                    id=str(artifact_identifier.artifact_version_id), paths=paths
                )
            )
            signed_urls = signed_urls_response.signed_urls
        elif artifact_identifier.dataset_fqn:
            signed_urls_dataset_response = self._mlfoundry_artifacts_api.get_signed_urls_for_dataset_write_post(
                get_signed_url_for_dataset_write_request_dto=GetSignedURLForDatasetWriteRequestDto(
                    dataset_fqn=artifact_identifier.dataset_fqn, paths=paths
                )
            )
            signed_urls = signed_urls_dataset_response.signed_urls
        else:
            raise ValueError(
                "Invalid artifact type - both `artifact_version_id` and `dataset_fqn` both are None"
            )
        return signed_urls

    def _normal_upload(
        self,
        local_file: str,
        artifact_path: str,
        signed_url: Optional[SignedURLDto],
        progress_bar: Progress,
        abort_event: Optional[Event] = None,
    ):
        if not signed_url:
            signed_url = self.get_signed_urls_for_write(
                artifact_identifier=self.artifact_identifier, paths=[artifact_path]
            )[0]

        if progress_bar.disable:
            logger.info(
                "Uploading %s to %s",
                local_file,
                artifact_path,
            )

        _signed_url_upload_file(
            signed_url=signed_url,
            local_file=local_file,
            abort_event=abort_event,
            progress_bar=progress_bar,
        )
        logger.debug("Uploaded %s to %s", local_file, artifact_path)

    def _create_multipart_upload_for_identifier(
        self,
        artifact_identifier: ArtifactIdentifier,
        path,
        num_parts,
    ) -> MultiPartUploadDto:
        if artifact_identifier.artifact_version_id:
            create_multipart_response: MultiPartUploadResponseDto = self._mlfoundry_artifacts_api.create_multi_part_upload_post(
                create_multi_part_upload_request_dto=CreateMultiPartUploadRequestDto(
                    artifact_version_id=str(artifact_identifier.artifact_version_id),
                    path=path,
                    num_parts=num_parts,
                )
            )
            multipart_upload = create_multipart_response.multipart_upload
        elif artifact_identifier.dataset_fqn:
            create_multipart_for_dataset_response = self._mlfoundry_artifacts_api.create_multipart_upload_for_dataset_post(
                create_multi_part_upload_for_dataset_request_dto=CreateMultiPartUploadForDatasetRequestDto(
                    dataset_fqn=artifact_identifier.dataset_fqn,
                    path=path,
                    num_parts=num_parts,
                )
            )
            multipart_upload = create_multipart_for_dataset_response.multipart_upload
        else:
            raise ValueError(
                "Invalid artifact type - both `artifact_version_id` and `dataset_fqn` both are None"
            )
        return multipart_upload

    def _multipart_upload(
        self,
        local_file: str,
        artifact_path: str,
        multipart_info: _FileMultiPartInfo,
        executor: ThreadPoolExecutor,
        progress_bar: Progress,
        abort_event: Optional[Event] = None,
    ):
        if progress_bar.disable:
            logger.info(
                "Uploading %s to %s using multipart upload",
                local_file,
                artifact_path,
            )

        multipart_upload = self._create_multipart_upload_for_identifier(
            artifact_identifier=self.artifact_identifier,
            path=artifact_path,
            num_parts=multipart_info.num_parts,
        )
        if (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.S3_COMPATIBLE
        ):
            _s3_compatible_multipart_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
                progress_bar=progress_bar,
            )
        elif (
            multipart_upload.storage_provider
            is MultiPartUploadStorageProvider.AZURE_BLOB
        ):
            _azure_multi_part_upload(
                multipart_upload=multipart_upload,
                local_file=local_file,
                executor=executor,
                multipart_info=multipart_info,
                abort_event=abort_event,
                progress_bar=progress_bar,
            )
        else:
            raise NotImplementedError()

    def _upload_file(
        self,
        local_file: str,
        artifact_path: str,
        multipart_info: _FileMultiPartInfo,
        progress_bar: Progress,
        signed_url: Optional[SignedURLDto] = None,
        abort_event: Optional[Event] = None,
        executor_for_multipart_upload: Optional[ThreadPoolExecutor] = None,
    ):
        if multipart_info.num_parts == 1:
            return self._normal_upload(
                local_file=local_file,
                artifact_path=artifact_path,
                signed_url=signed_url,
                abort_event=abort_event,
                progress_bar=progress_bar,
            )

        if not executor_for_multipart_upload:
            with ThreadPoolExecutor(
                max_workers=ENV_VARS.TFY_ARTIFACTS_UPLOAD_MAX_WORKERS
            ) as executor:
                return self._multipart_upload(
                    local_file=local_file,
                    artifact_path=artifact_path,
                    executor=executor,
                    multipart_info=multipart_info,
                    progress_bar=progress_bar,
                )

        return self._multipart_upload(
            local_file=local_file,
            artifact_path=artifact_path,
            executor=executor_for_multipart_upload,
            multipart_info=multipart_info,
            progress_bar=progress_bar,
        )

    def _upload(
        self,
        files_for_normal_upload: Sequence[Tuple[str, str, _FileMultiPartInfo]],
        files_for_multipart_upload: Sequence[Tuple[str, str, _FileMultiPartInfo]],
        progress: Optional[bool] = None,
    ):
        abort_event = Event()
        show_progress = _can_display_progress(progress)
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            refresh_per_second=1,
            disable=not show_progress,
            expand=True,
        ) as progress_bar, ThreadPoolExecutor(
            max_workers=ENV_VARS.TFY_ARTIFACTS_UPLOAD_MAX_WORKERS
        ) as executor:
            futures: List[Future] = []
            # Note: While this batching is beneficial when there is a large number of files, there is also
            # a rare case risk of the signed url expiring before a request is made to it
            _batch_size = _GENERATE_SIGNED_URL_BATCH_SIZE
            for start_idx in range(0, len(files_for_normal_upload), _batch_size):
                end_idx = min(start_idx + _batch_size, len(files_for_normal_upload))
                if _any_future_has_failed(futures):
                    break
                logger.debug("Generating write signed urls for a batch ...")
                remote_file_paths = [
                    files_for_normal_upload[idx][0] for idx in range(start_idx, end_idx)
                ]
                signed_urls = self.get_signed_urls_for_write(
                    artifact_identifier=self.artifact_identifier,
                    paths=remote_file_paths,
                )
                for idx, signed_url in zip(range(start_idx, end_idx), signed_urls):
                    (
                        upload_path,
                        local_file,
                        multipart_info,
                    ) = files_for_normal_upload[idx]
                    future = executor.submit(
                        self._upload_file,
                        local_file=local_file,
                        artifact_path=upload_path,
                        multipart_info=multipart_info,
                        signed_url=signed_url,
                        abort_event=abort_event,
                        executor_for_multipart_upload=None,
                        progress_bar=progress_bar,
                    )
                    futures.append(future)

            done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
            if len(not_done) > 0:
                abort_event.set()
            for future in not_done:
                future.cancel()
            for future in done:
                if future.exception() is not None:
                    raise future.exception()

            for (
                upload_path,
                local_file,
                multipart_info,
            ) in files_for_multipart_upload:
                self._upload_file(
                    local_file=local_file,
                    artifact_path=upload_path,
                    signed_url=None,
                    multipart_info=multipart_info,
                    executor_for_multipart_upload=executor,
                    progress_bar=progress_bar,
                )

    def _add_file_for_upload(
        self,
        local_file: str,
        artifact_path: str,
        files_for_normal_upload: List[Tuple[str, str, _FileMultiPartInfo]],
        files_for_multipart_upload: List[Tuple[str, str, _FileMultiPartInfo]],
    ):
        local_file = os.path.realpath(local_file)
        if os.path.isdir(local_file):
            raise MlFoundryException(
                "Cannot log a directory as an artifact. Use `log_artifacts` instead"
            )
        upload_path = artifact_path
        upload_path = upload_path.lstrip(posixpath.sep)
        multipart_info = _decide_file_parts(local_file)
        if multipart_info.num_parts == 1:
            files_for_normal_upload.append((upload_path, local_file, multipart_info))
        else:
            files_for_multipart_upload.append((upload_path, local_file, multipart_info))

    def _add_dir_for_upload(
        self,
        local_dir: str,
        artifact_path: str,
        files_for_normal_upload: List[Tuple[str, str, _FileMultiPartInfo]],
        files_for_multipart_upload: List[Tuple[str, str, _FileMultiPartInfo]],
    ):
        local_dir = os.path.realpath(local_dir)
        if not os.path.isdir(local_dir):
            raise MlFoundryException(
                "Cannot log a file as a directory. Use `log_artifact` instead"
            )
        dest_path = artifact_path
        dest_path = dest_path.lstrip(posixpath.sep)

        for root, _, file_names in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                self._add_file_for_upload(
                    local_file=local_file,
                    artifact_path=upload_path,
                    files_for_normal_upload=files_for_normal_upload,
                    files_for_multipart_upload=files_for_multipart_upload,
                )

    def log_artifacts(
        self,
        src_dest_pairs: Sequence[Tuple[str, Optional[str]]],
        progress: Optional[bool] = None,
    ):
        files_for_normal_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []
        files_for_multipart_upload: List[Tuple[str, str, _FileMultiPartInfo]] = []
        for src, dest in src_dest_pairs:
            if os.path.isdir(src):
                self._add_dir_for_upload(
                    local_dir=src,
                    artifact_path=dest or "",
                    files_for_normal_upload=files_for_normal_upload,
                    files_for_multipart_upload=files_for_multipart_upload,
                )
            else:
                self._add_file_for_upload(
                    local_file=src,
                    artifact_path=dest or "",
                    files_for_normal_upload=files_for_normal_upload,
                    files_for_multipart_upload=files_for_multipart_upload,
                )
        self._upload(
            files_for_normal_upload=files_for_normal_upload,
            files_for_multipart_upload=files_for_multipart_upload,
            progress=progress,
        )

    def _list_files(
        self, artifact_identifier: ArtifactIdentifier, path, page_size, page_token
    ) -> Union[ListFilesForDatasetResponseDto, ListFilesForArtifactVersionsResponseDto]:
        if artifact_identifier.dataset_fqn:
            return self._mlfoundry_artifacts_api.list_files_for_dataset_post(
                list_files_for_dataset_request_dto=ListFilesForDatasetRequestDto(
                    dataset_fqn=artifact_identifier.dataset_fqn,
                    path=path,
                    max_results=page_size,
                    page_token=page_token,
                )
            )
        else:
            return self._mlfoundry_artifacts_api.list_files_for_artifact_version_post(
                list_files_for_artifact_version_request_dto=ListFilesForArtifactVersionRequestDto(
                    id=str(artifact_identifier.artifact_version_id),
                    path=path,
                    max_results=page_size,
                    page_token=page_token,
                )
            )

    def list_artifacts(
        self, path=None, page_size=_LIST_FILES_PAGE_SIZE, **kwargs
    ) -> Iterator[FileInfoDto]:
        page_token = None
        started = False
        while not started or page_token is not None:
            started = True
            page = self._list_files(
                artifact_identifier=self.artifact_identifier,
                path=path,
                page_size=page_size,
                page_token=page_token,
            )
            for file_info in page.files:
                yield file_info
            page_token = page.next_page_token

    def _is_directory(self, artifact_path):
        # TODO: Ideally server should return a flag to indicate if it is a directory
        # For now we can rely on list_artifacts because generally in cloud buckets
        # directories are not stored as separate entities - empty directories ideally do not exist
        for _ in self.list_artifacts(artifact_path, page_size=3):
            return True
        return False

    def _create_download_destination(
        self, src_artifact_path: str, dst_local_dir_path: str
    ) -> str:
        """
        Creates a local filesystem location to be used as a destination for downloading the artifact
        specified by `src_artifact_path`. The destination location is a subdirectory of the
        specified `dst_local_dir_path`, which is determined according to the structure of
        `src_artifact_path`. For example, if `src_artifact_path` is `dir1/file1.txt`, then the
        resulting destination path is `<dst_local_dir_path>/dir1/file1.txt`. Local directories are
        created for the resulting destination location if they do not exist.

        :param src_artifact_path: A relative, POSIX-style path referring to an artifact stored
                                  within the repository's artifact root location.
                                  `src_artifact_path` should be specified relative to the
                                  repository's artifact root location.
        :param dst_local_dir_path: The absolute path to a local filesystem directory in which the
                                   local destination path will be contained. The local destination
                                   path may be contained in a subdirectory of `dst_root_dir` if
                                   `src_artifact_path` contains subdirectories.
        :return: The absolute path to a local filesystem location to be used as a destination
                 for downloading the artifact specified by `src_artifact_path`.
        """
        src_artifact_path = src_artifact_path.rstrip(
            "/"
        )  # Ensure correct dirname for trailing '/'
        dirpath = posixpath.dirname(src_artifact_path)
        local_dir_path = os.path.join(dst_local_dir_path, dirpath)
        local_file_path = os.path.join(dst_local_dir_path, src_artifact_path)
        if not os.path.exists(local_dir_path):
            os.makedirs(local_dir_path, exist_ok=True)
        return local_file_path

    # noinspection PyMethodOverriding
    def _download_file(
        self,
        remote_file_path: str,
        local_path: str,
        progress_bar: Optional[Progress],
        signed_url: Optional[SignedURLDto],
        abort_event: Optional[Event] = None,
    ):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )
        if not signed_url:
            signed_url = self.get_signed_urls_for_read(
                artifact_identifier=self.artifact_identifier, paths=[remote_file_path]
            )[0]

        if progress_bar is None or not progress_bar.disable:
            logger.info("Downloading %s to %s", remote_file_path, local_path)

        if progress_bar is not None:
            download_progress_bar = progress_bar.add_task(
                f"[green]Downloading to {remote_file_path}:", start=True
            )

        def callback(chunk, total_file_size):
            if progress_bar is not None:
                progress_bar.update(
                    download_progress_bar,
                    advance=chunk,
                    total=total_file_size,
                )
            if abort_event and abort_event.is_set():
                raise Exception("aborting download")

        _download_file_using_http_uri(
            http_uri=signed_url.signed_url,
            download_path=local_path,
            callback=callback,
        )
        logger.debug("Downloaded %s to %s", remote_file_path, local_path)

    def _download_artifact(
        self,
        src_artifact_path: str,
        dst_local_dir_path: str,
        signed_url: Optional[SignedURLDto],
        progress_bar: Optional[Progress] = None,
        abort_event=None,
    ) -> str:
        """
        Download the file artifact specified by `src_artifact_path` to the local filesystem
        directory specified by `dst_local_dir_path`.
        :param src_artifact_path: A relative, POSIX-style path referring to a file artifact
                                    stored within the repository's artifact root location.
                                    `src_artifact_path` should be specified relative to the
                                    repository's artifact root location.
        :param dst_local_dir_path: Absolute path of the local filesystem destination directory
                                    to which to download the specified artifact. The downloaded
                                    artifact may be written to a subdirectory of
                                    `dst_local_dir_path` if `src_artifact_path` contains
                                    subdirectories.
        :param progress_bar: An instance of a Rich progress bar used to visually display the
                              progress of the file download.
        :return: A local filesystem path referring to the downloaded file.
        """
        local_destination_file_path = self._create_download_destination(
            src_artifact_path=src_artifact_path, dst_local_dir_path=dst_local_dir_path
        )
        self._download_file(
            remote_file_path=src_artifact_path,
            local_path=local_destination_file_path,
            signed_url=signed_url,
            abort_event=abort_event,
            progress_bar=progress_bar,
        )
        return local_destination_file_path

    def _get_file_paths_recur(self, src_artifact_dir_path, dst_local_dir_path):
        local_dir = os.path.join(dst_local_dir_path, src_artifact_dir_path)
        # prevent infinite loop, sometimes the dir is recursively included
        # TODO (chiragjn): Check why and when this happens
        dir_content = [
            file_info
            for file_info in self.list_artifacts(src_artifact_dir_path)
            if file_info.path != "." and file_info.path != src_artifact_dir_path
        ]
        if not dir_content:  # empty dir
            if not os.path.exists(local_dir):
                os.makedirs(local_dir, exist_ok=True)
        else:
            for file_info in dir_content:
                if file_info.is_dir:
                    yield from self._get_file_paths_recur(
                        src_artifact_dir_path=file_info.path,
                        dst_local_dir_path=dst_local_dir_path,
                    )
                else:
                    yield file_info.path, dst_local_dir_path

    def download_artifacts(  # noqa: C901
        self,
        artifact_path: str,
        dst_path: Optional[str] = None,
        overwrite: bool = False,
        progress: Optional[bool] = None,
    ) -> str:
        """
        Download an artifact file or directory to a local directory if applicable, and return a
        local path for it. The caller is responsible for managing the lifecycle of the downloaded artifacts.

        Args:
            artifact_path: Relative source path to the desired artifacts.
            dst_path: Absolute path of the local filesystem destination directory to which to
                download the specified artifacts. This directory must already exist.
                If unspecified, the artifacts will either be downloaded to a new
                uniquely-named directory.
            overwrite: if to overwrite the files at/inside `dst_path` if they exist
            progress: Show or hide progress bar

        Returns:
            str: Absolute path of the local filesystem location containing the desired artifacts.
        """

        show_progress = _can_display_progress(user_choice=progress)

        is_dir_temp = False
        if dst_path is None:
            dst_path = tempfile.mkdtemp()
            is_dir_temp = True

        dst_path = os.path.abspath(dst_path)
        if is_dir_temp:
            logger.info(
                f"Using temporary directory {dst_path} as the download directory"
            )

        if not os.path.exists(dst_path):
            raise MlFoundryException(
                message=(
                    "The destination path for downloaded artifacts does not"
                    " exist! Destination path: {dst_path}".format(dst_path=dst_path)
                ),
            )
        elif not os.path.isdir(dst_path):
            raise MlFoundryException(
                message=(
                    "The destination path for downloaded artifacts must be a directory!"
                    " Destination path: {dst_path}".format(dst_path=dst_path)
                ),
            )

        progress_bar = Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            TimeElapsedColumn(),
            refresh_per_second=1,
            disable=not show_progress,
            expand=True,
        )

        try:
            progress_bar.start()
            # empty string is treated as root directory
            if not artifact_path or self._is_directory(artifact_path):
                futures: List[Future] = []
                file_paths: List[Tuple[str, str]] = []
                abort_event = Event()

                # Check if any file is being overwritten before downloading them
                for file_path, download_dest_path in self._get_file_paths_recur(
                    src_artifact_dir_path=artifact_path, dst_local_dir_path=dst_path
                ):
                    final_file_path = os.path.join(download_dest_path, file_path)

                    # There would be no overwrite if temp directory is being used
                    if (
                        not is_dir_temp
                        and os.path.exists(final_file_path)
                        and not overwrite
                    ):
                        raise MlFoundryException(
                            f"File already exists at {final_file_path}, aborting download "
                            f"(set `overwrite` flag to overwrite this and any subsequent files)"
                        )
                    file_paths.append((file_path, download_dest_path))

                with ThreadPoolExecutor(
                    max_workers=ENV_VARS.TFY_ARTIFACTS_DOWNLOAD_MAX_WORKERS
                ) as executor:
                    # Note: While this batching is beneficial when there is a large number of files, there is also
                    # a rare case risk of the signed url expiring before a request is made to it
                    batch_size = _GENERATE_SIGNED_URL_BATCH_SIZE
                    for start_idx in range(0, len(file_paths), batch_size):
                        end_idx = min(start_idx + batch_size, len(file_paths))
                        if _any_future_has_failed(futures):
                            break
                        logger.debug("Generating read signed urls for a batch ...")
                        remote_file_paths = [
                            file_paths[idx][0] for idx in range(start_idx, end_idx)
                        ]
                        signed_urls = self.get_signed_urls_for_read(
                            artifact_identifier=self.artifact_identifier,
                            paths=remote_file_paths,
                        )
                        for idx, signed_url in zip(
                            range(start_idx, end_idx), signed_urls
                        ):
                            file_path, download_dest_path = file_paths[idx]
                            future = executor.submit(
                                self._download_artifact,
                                src_artifact_path=file_path,
                                dst_local_dir_path=download_dest_path,
                                signed_url=signed_url,
                                abort_event=abort_event,
                                progress_bar=progress_bar,
                            )
                            futures.append(future)

                    done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
                    if len(not_done) > 0:
                        abort_event.set()
                    for future in not_done:
                        future.cancel()
                    for future in done:
                        if future.exception() is not None:
                            raise future.exception()

                    output_dir = os.path.join(dst_path, artifact_path)
                    return output_dir
            else:
                return self._download_artifact(
                    src_artifact_path=artifact_path,
                    dst_local_dir_path=dst_path,
                    signed_url=None,
                    progress_bar=progress_bar,
                )
        except Exception as err:
            if is_dir_temp:
                logger.info(
                    f"Error encountered, removing temporary download directory at {dst_path}"
                )
                rmtree(dst_path)  # remove temp directory alongside it's contents
            raise err

        finally:
            progress_bar.stop()
