import time
from functools import lru_cache, wraps
from time import monotonic_ns
from typing import Callable, Generator, Optional, TypeVar
from urllib.parse import urljoin, urlparse

from truefoundry.common.constants import (
    API_SERVER_RELATIVE_PATH,
    ENV_VARS,
    MLFOUNDRY_SERVER_RELATIVE_PATH,
    TFY_HOST_ENV_KEY,
)
from truefoundry.pydantic_v1 import BaseSettings

T = TypeVar("T")


class _TFYServersConfig(BaseSettings):
    class Config:
        env_prefix = "TFY_CLI_LOCAL_"
        env_file = ".tfy-cli-local.env"

    tenant_host: str
    servicefoundry_server_url: str
    mlfoundry_server_url: str

    @classmethod
    def from_base_url(cls, base_url: str) -> "_TFYServersConfig":
        base_url = base_url.strip("/")
        return cls(
            tenant_host=urlparse(base_url).netloc,
            servicefoundry_server_url=urljoin(base_url, API_SERVER_RELATIVE_PATH),
            mlfoundry_server_url=urljoin(base_url, MLFOUNDRY_SERVER_RELATIVE_PATH),
        )


_tfy_servers_config = None


def get_tfy_servers_config(base_url: str) -> _TFYServersConfig:
    global _tfy_servers_config
    if _tfy_servers_config is None:
        if ENV_VARS.TFY_CLI_LOCAL_DEV_MODE:
            _tfy_servers_config = _TFYServersConfig()  # type: ignore[call-arg]
        else:
            _tfy_servers_config = _TFYServersConfig.from_base_url(base_url)
    return _tfy_servers_config


def relogin_error_message(message: str, host: str = "HOST") -> str:
    suffix = ""
    if host == "HOST":
        suffix = " where HOST is TrueFoundry platform URL"
    return (
        f"{message}\n"
        f"Please login again using `tfy login --host {host} --relogin` "
        f"or `truefoundry.login(host={host!r}, relogin=True)` function" + suffix
    )


def timed_lru_cache(
    seconds: int = 300, maxsize: Optional[int] = None
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def wrapper_cache(func: Callable[..., T]) -> Callable[..., T]:
        func = lru_cache(maxsize=maxsize)(func)
        func.delta = seconds * 10**9
        func.expiration = monotonic_ns() + func.delta

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if monotonic_ns() >= func.expiration:
                func.cache_clear()
                func.expiration = monotonic_ns() + func.delta
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def poll_for_function(
    func: Callable[..., T], poll_after_secs: int = 5, *args, **kwargs
) -> Generator[T, None, None]:
    while True:
        yield func(*args, **kwargs)
        time.sleep(poll_after_secs)


def validate_tfy_host(tfy_host: str) -> None:
    if not (tfy_host.startswith("https://") or tfy_host.startswith("http://")):
        raise ValueError(
            f"Invalid host {tfy_host!r}. It should start with https:// or http://"
        )


def resolve_tfy_host(tfy_host: Optional[str] = None) -> str:
    if not tfy_host and not ENV_VARS.TFY_HOST:
        raise ValueError(
            f"Either `host` should be provided using `--host <value>`, or `{TFY_HOST_ENV_KEY}` env must be set"
        )
    tfy_host = tfy_host or ENV_VARS.TFY_HOST
    tfy_host = tfy_host.strip("/")
    validate_tfy_host(tfy_host)
    return tfy_host
