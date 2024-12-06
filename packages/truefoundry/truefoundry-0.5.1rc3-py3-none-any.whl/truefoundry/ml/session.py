import atexit
import threading
import weakref
from typing import TYPE_CHECKING, Dict, Optional

from truefoundry.common.credential_provider import (
    CredentialProvider,
    EnvCredentialProvider,
    FileCredentialProvider,
)
from truefoundry.common.entities import Token, UserInfo
from truefoundry.common.request_utils import urllib3_retry
from truefoundry.common.utils import get_tfy_servers_config, relogin_error_message
from truefoundry.ml.autogen.client import (  # type: ignore[attr-defined]
    ApiClient,
    Configuration,
)
from truefoundry.ml.clients.entities import HostCreds
from truefoundry.ml.exceptions import MlFoundryException
from truefoundry.ml.logger import logger

if TYPE_CHECKING:
    from truefoundry.ml.mlfoundry_run import MlFoundryRun

SESSION_LOCK = threading.RLock()


class ActiveRuns:
    def __init__(self):
        self._active_runs: Dict[str, weakref.ReferenceType["MlFoundryRun"]] = {}

    def add_run(self, run: "MlFoundryRun"):
        with SESSION_LOCK:
            self._active_runs[run.run_id] = weakref.ref(run)

    def remove_run(self, run: "MlFoundryRun"):
        with SESSION_LOCK:
            if run.run_id in self._active_runs:
                del self._active_runs[run.run_id]

    def close_active_runs(self):
        with SESSION_LOCK:
            for run_ref in list(self._active_runs.values()):
                run = run_ref()
                if run and run.auto_end:
                    run.end()
            self._active_runs.clear()


ACTIVE_RUNS = ActiveRuns()
atexit.register(ACTIVE_RUNS.close_active_runs)


class Session:
    def __init__(self, cred_provider: CredentialProvider):
        # Note: Whenever a new session is initialized all the active runs are ended
        self._closed = False
        self._cred_provider: Optional[CredentialProvider] = cred_provider
        self._user_info: Optional[UserInfo] = self._cred_provider.token.to_user_info()

    def close(self):
        logger.debug("Closing existing session")
        self._closed = True
        self._user_info = None
        self._cred_provider = None

    def _assert_not_closed(self):
        if self._closed:
            raise MlFoundryException(
                "This session has been deactivated.\n"
                "At a time only one `client` (received from "
                "`truefoundry.ml.get_client()` function call) can be used"
            )

    @property
    def token(self) -> Token:
        return self._cred_provider.token

    @property
    def user_info(self) -> UserInfo:
        self._assert_not_closed()
        return self._user_info

    # TODO (chiragjn): Rename tracking_uri to tfy_host
    @property
    def tracking_uri(self) -> str:
        return self._cred_provider.base_url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return False
        return (
            type(self._cred_provider) == type(other._cred_provider)  # noqa: E721
            and self.user_info == other.user_info
            and self.tracking_uri == other.tracking_uri
        )

    def get_host_creds(self) -> HostCreds:
        tracking_uri = get_tfy_servers_config(self.tracking_uri).mlfoundry_server_url
        return HostCreds(
            host=tracking_uri, token=self._cred_provider.token.access_token
        )


ACTIVE_SESSION: Optional[Session] = None


def get_active_session() -> Optional[Session]:
    return ACTIVE_SESSION


def _get_api_client(
    session: Optional[Session] = None,
    allow_anonymous: bool = False,
) -> ApiClient:
    from truefoundry.version import __version__

    session = session or get_active_session()
    if session is None:
        if allow_anonymous:
            return ApiClient()
        else:
            raise MlFoundryException(
                relogin_error_message(
                    "No active session found. Perhaps you are not logged in?",
                )
            )

    creds = session.get_host_creds()
    configuration = Configuration(
        host=creds.host.rstrip("/"),
        access_token=creds.token,
    )
    configuration.retries = urllib3_retry(retries=2)
    api_client = ApiClient(configuration=configuration)
    api_client.user_agent = f"truefoundry-cli/{__version__}"
    return api_client


def init_session() -> Session:
    with SESSION_LOCK:
        final_cred_provider = None
        for cred_provider in [EnvCredentialProvider, FileCredentialProvider]:
            if cred_provider.can_provide():
                final_cred_provider = cred_provider()
                break
        if final_cred_provider is None:
            raise MlFoundryException(
                relogin_error_message(
                    "No active session found. Perhaps you are not logged in?",
                )
            )
        new_session = Session(cred_provider=final_cred_provider)

        global ACTIVE_SESSION
        if ACTIVE_SESSION and ACTIVE_SESSION == new_session:
            return ACTIVE_SESSION

        ACTIVE_RUNS.close_active_runs()

        if ACTIVE_SESSION:
            ACTIVE_SESSION.close()
        ACTIVE_SESSION = new_session

        logger.info(
            "Logged in to %r as %r (%s)",
            ACTIVE_SESSION.tracking_uri,
            ACTIVE_SESSION.user_info.user_id,
            ACTIVE_SESSION.user_info.email or ACTIVE_SESSION.user_info.user_type.value,
        )
        return ACTIVE_SESSION
