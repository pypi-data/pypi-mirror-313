import json
from contextlib import contextmanager
from typing import Any, Optional
from urllib.parse import urljoin

import requests

from truefoundry.common.request_utils import requests_retry_session
from truefoundry.ml.clients.entities import HostCreds
from truefoundry.ml.exceptions import MlFoundryException


# TODO: This will be moved later to truefoundry.common.request_utils
def _make_url(host: str, endpoint: str) -> str:
    if endpoint.startswith("/"):
        raise ValueError("`endpoint` must not start with a leading slash (/)")
    return urljoin(host, endpoint)


def _http_request(
    *, method: str, url: str, token: Optional[str] = None, session=requests, **kwargs
) -> requests.Response:
    headers = kwargs.pop("headers", {}) or {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    return session.request(method=method, url=url, headers=headers, **kwargs)


def http_request(
    *, method: str, host_creds: HostCreds, endpoint: str, session=requests, **kwargs
) -> requests.Response:
    url = _make_url(host=host_creds.host, endpoint=endpoint)
    return _http_request(
        method=method, url=url, token=host_creds.token, session=session, **kwargs
    )


def http_request_safe(
    *, method: str, host_creds: HostCreds, endpoint: str, session=requests, **kwargs
) -> Any:
    url = _make_url(host=host_creds.host, endpoint=endpoint)
    try:
        response = _http_request(
            method=method, url=url, token=host_creds.token, session=session, **kwargs
        )
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError as je:
            raise MlFoundryException(
                f"Failed to parse response as json. Response: {response.text}"
            ) from je
    except requests.exceptions.ConnectionError as ce:
        raise MlFoundryException("Failed to connect to TrueFoundry") from ce
    except requests.exceptions.Timeout as te:
        raise MlFoundryException(f"Request to {url} timed out") from te
    except requests.exceptions.HTTPError as he:
        raise MlFoundryException(
            f"Request to {url} with status code {he.response.status_code}. Response: {he.response.text}",
            status_code=he.response.status_code,
        ) from he
    except Exception as e:
        raise MlFoundryException(
            f"Request to {url} failed with an unknown error"
        ) from e


@contextmanager
def cloud_storage_http_request(
    *,
    method,
    url,
    session=None,
    timeout=None,
    **kwargs,
):
    """
    Performs an HTTP PUT/GET request using Python's `requests` module with automatic retry.
    """
    session = session or requests_retry_session(retries=5, backoff_factor=0.5)
    kwargs["headers"] = kwargs.get("headers", {}) or {}
    if "blob.core.windows.net" in url:
        kwargs["headers"].update({"x-ms-blob-type": "BlockBlob"})
    if method.lower() not in ("put", "get"):
        raise ValueError(f"Illegal http method: {method}")
    try:
        yield _http_request(
            method=method, url=url, session=session, timeout=timeout, **kwargs
        )
    except Exception as e:
        raise MlFoundryException(
            f"API request failed with exception {str(e)}"
        ) from None


def augmented_raise_for_status(response):
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as he:
        raise MlFoundryException(
            f"Request with status code {he.response.status_code}. Response: {he.response.text}",
            status_code=he.response.status_code,
        ) from he


def download_file_using_http_uri(http_uri, download_path, chunk_size=100_000_000):
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
        with open(download_path, "wb") as output_file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not chunk:
                    break
                output_file.write(chunk)
