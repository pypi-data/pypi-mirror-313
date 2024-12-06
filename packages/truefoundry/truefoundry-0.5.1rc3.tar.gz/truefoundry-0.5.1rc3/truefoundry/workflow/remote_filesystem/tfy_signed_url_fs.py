# file: tfy_signed_url_fs.py
# pylint: disable=W0223
import io
import os
from pathlib import Path
from typing import Optional

from fsspec.spec import DEFAULT_CALLBACK, AbstractBufferedFile, AbstractFileSystem

from truefoundry.common.constants import ENV_VARS
from truefoundry.workflow.remote_filesystem.logger import log_time
from truefoundry.workflow.remote_filesystem.tfy_signed_url_client import (
    LOG_PREFIX,
    SignedURLClient,
)


class SignedURLFileSystem(AbstractFileSystem):
    def __init__(
        self, base_url: Optional[str] = None, token: Optional[str] = None, **kwargs
    ):
        super().__init__()
        base_url = base_url or ENV_VARS.TFY_INTERNAL_SIGNED_URL_SERVER_HOST
        token = token or ENV_VARS.TFY_INTERNAL_SIGNED_URL_SERVER_TOKEN
        self.client = SignedURLClient(base_url, token)

    @log_time(prefix=LOG_PREFIX)
    def exists(self, path, **kwargs):
        """Check if a file exists at the given path."""
        return self.client.exists(path)

    @log_time(prefix=LOG_PREFIX)
    def get(
        self,
        rpath,
        lpath,
        recursive=False,
        callback=DEFAULT_CALLBACK,
        maxdepth=None,
        **kwargs,
    ):
        """Get file(s) to local"""
        # TODO: Add support for ThreadPoolExecutor here
        # TODO: Add support for async download
        # TODO: Do a proper error handling here
        if self.isdir(rpath):
            if not recursive:
                raise ValueError(
                    f"{rpath} is a directory, but recursive is not enabled."
                )

            # Handle recursive download
            files = self.ls(rpath, detail=True)

            for file_info in files:
                file_path = file_info.path.rstrip("/").rsplit("/")[-1]

                is_directory = file_info.is_directory
                # Construct the relative path for local download
                relative_path = rpath.rstrip("/") + "/" + file_path
                target_local_path = lpath.rstrip("/") + "/" + file_path

                if is_directory:
                    # If it's a directory, create the directory locally
                    Path(target_local_path).mkdir(parents=True, exist_ok=True)
                    relative_path = relative_path + "/"
                    if recursive:
                        # Recursively download the contents of the directory
                        self.get(
                            relative_path,
                            target_local_path,
                            recursive=True,
                            maxdepth=maxdepth,
                            **kwargs,
                        )
                else:
                    self.client.download(
                        storage_uri=relative_path, local_path=target_local_path
                    )

        else:
            # Ensure the directory exists first
            target_local_path = lpath
            if target_local_path.endswith("/"):
                # If it ends with "/", it's a directory, so create the directory first
                target_local_path = os.path.join(
                    target_local_path, rpath.rsplit("/", 1)[-1]
                )
            # Create the directory for the target file path (common for both cases)
            Path(os.path.dirname(target_local_path)).mkdir(parents=True, exist_ok=True)
            self.client.download(storage_uri=rpath, local_path=target_local_path)

    @log_time(prefix=LOG_PREFIX)
    def put(
        self,
        lpath,
        rpath,
        recursive=False,
        callback=DEFAULT_CALLBACK,
        maxdepth=None,
        **kwargs,
    ):
        local_path = Path(lpath)
        if local_path.is_dir():
            if not recursive:
                raise ValueError(
                    f"{lpath} is a directory, but recursive is set to False."
                )

            # Optionally limit recursion depth
            max_depth = maxdepth if maxdepth is not None else float("inf")

            # Walk through the directory structure
            for root, _, files in os.walk(lpath):
                current_depth = Path(root).relative_to(local_path).parts
                if len(current_depth) > max_depth:
                    continue  # Skip files deeper than the max depth

                rel_dir = Path(root).relative_to(local_path)
                remote_dir = (
                    rpath.rstrip("/")
                    if rel_dir == Path(".")
                    else rpath.rstrip("/") + "/" + str(rel_dir)
                )

                # Upload each file
                for file in files:
                    local_file_path = Path(root) / file
                    remote_file_path = f"{remote_dir}/{file}"
                    self.client.upload(
                        file_path=str(local_file_path),
                        storage_uri=remote_file_path,
                    )
            return None
        else:
            if rpath.endswith("/"):
                rpath = os.path.join(rpath, local_path.name)
            return self.client.upload(file_path=lpath, storage_uri=rpath)

    @log_time(prefix=LOG_PREFIX)
    def isdir(self, path):
        """Is this entry directory-like?"""
        return self.client.is_directory(path)

    def open(
        self,
        path,
        mode="rb",
        block_size=None,
        cache_options=None,
        compression=None,
        **kwargs,
    ):
        """
        Open a file for reading or writing.
        """
        if "r" in mode:
            # Reading mode
            file_content = self.client.download_to_bytes(path)
            return io.BytesIO(file_content)
        elif "w" in mode or "a" in mode:
            # Writing mode (appending treated as writing)
            buffer = io.BytesIO()
            buffer.seek(0)

            def on_close(buffer=buffer, path=path):
                """
                Callback when file is closed, automatically upload the content.
                """
                buffer.seek(0)
                self.client.upload_from_bytes(buffer.read(), storage_uri=path)

            # Wrapping the buffer to automatically upload on close
            return io.BufferedWriter(buffer, on_close)

    @log_time(prefix=LOG_PREFIX)
    def write(self, path, data, **kwargs):
        """
        Write data to the file at the specified path (this could be tied to open's close).
        """
        if isinstance(data, io.BytesIO):
            data.seek(0)
            content = data.read()
        elif isinstance(data, str):
            content = data.encode()  # Encode to bytes
        else:
            raise ValueError("Unsupported data type for writing")

        # Upload the content to the remote file system
        self.client.upload_from_bytes(content, storage_uri=path)

    @log_time(prefix=LOG_PREFIX)
    def ls(self, path, detail=True, **kwargs):
        """List objects at path."""
        return self.client.list_files(path, detail=detail)


class SignedURLBufferedFile(AbstractBufferedFile):
    """
    Buffered file implementation for Signed URL-based file system.
    # TODO: Need to test this implementation
    """

    def __init__(
        self, fs: SignedURLFileSystem, path: str, mode: str, block_size: int, **kwargs
    ):
        """
        Initialize the buffered file, determining the mode (read/write).
        """
        super().__init__(fs, path, mode, block_size, **kwargs)
        self.buffer = io.BytesIO()
        self.client = fs.client

        if "r" in mode:
            # Download the file content for reading
            file_content = fs.client.download_to_bytes(path)
            self.buffer.write(file_content)
            self.buffer.seek(0)  # Reset buffer after writing content

    def _upload_on_close(self):
        """
        Upload content back to the remote store when the file is closed.
        """
        self.buffer.seek(0)
        self.client.upload_from_bytes(self.buffer.read(), storage_uri=self.path)

    def close(self):
        """
        Close the file, ensuring the content is uploaded for write/append modes.
        """
        if self.writable():
            self._upload_on_close()
        self.buffer.close()
        super().close()

    def _fetch_range(self, start, end):
        """
        Fetch a specific byte range from the file. Useful for large files and range reads.
        """
        self.buffer.seek(start)
        return self.buffer.read(end - start)

    def _upload_chunk(self, final=False):
        """
        Upload a chunk of the file. For larger files, data may be uploaded in chunks.
        """
        if final:
            self._upload_on_close()
