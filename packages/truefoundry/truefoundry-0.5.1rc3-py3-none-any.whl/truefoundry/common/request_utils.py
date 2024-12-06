from typing import Optional

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from truefoundry.common.exceptions import BadRequestException


def request_handling(response: Response):
    try:
        status_code = response.status_code
    except Exception as e:
        raise Exception("Unknown error occurred. Couldn't get status code.") from e
    if 200 <= status_code <= 299:
        if response.content == b"":
            return None
        return response.json()
    if 400 <= status_code <= 499:
        try:
            message = str(response.json()["message"])
        except Exception:
            message = response.text
        raise BadRequestException(status_code=response.status_code, message=message)
    if 500 <= status_code <= 599:
        raise Exception(response.content)


def urllib3_retry(
    retries: int = 2,
    backoff_factor: float = 0.3,
    status_forcelist=(408, 429, 500, 502, 503, 504, 524),
    method_whitelist=frozenset({"GET", "POST"}),
    raise_on_status: bool = False,
):
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        status=retries,
        backoff_factor=backoff_factor,
        allowed_methods=method_whitelist,
        status_forcelist=status_forcelist,
        respect_retry_after_header=True,
        raise_on_status=raise_on_status,
    )
    return retry


def requests_retry_session(
    retries: int = 2,
    backoff_factor: float = 0.3,
    status_forcelist=(408, 429, 417, 500, 502, 503, 504, 524),
    method_whitelist=frozenset({"GET", "POST"}),
    raise_on_status: bool = False,
    session: Optional[requests.Session] = None,
) -> requests.Session:
    """
    Returns a `requests` session with retry capabilities for certain HTTP status codes.

    Args:
        retries (int): The number of retries for HTTP requests.
        backoff_factor (float): The backoff factor for exponential backoff during retries.
        status_forcelist (tuple): A tuple of HTTP status codes that should trigger a retry.
        method_whitelist (frozenset): The set of HTTP methods that should be retried.
        session (requests.Session, optional): An optional existing requests session to use.

    Returns:
        requests.Session: A session with retry capabilities.
    """
    # Implementation taken from https://www.peterbe.com/plog/best-practice-with-retries-with-requests
    session = session or requests.Session()
    retry = urllib3_retry(
        retries=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=method_whitelist,
        raise_on_status=raise_on_status,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
