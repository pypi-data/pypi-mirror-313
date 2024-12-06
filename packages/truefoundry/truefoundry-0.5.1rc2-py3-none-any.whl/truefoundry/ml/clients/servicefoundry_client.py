from typing import Optional

from truefoundry.common.constants import (
    SERVICEFOUNDRY_CLIENT_MAX_RETRIES,
    VERSION_PREFIX,
)
from truefoundry.common.servicefoundry_client import (
    ServiceFoundryServiceClient as BaseServiceFoundryServiceClient,
)
from truefoundry.ml.clients.entities import (
    HostCreds,
)
from truefoundry.ml.clients.utils import http_request_safe
from truefoundry.ml.exceptions import MlFoundryException


class ServiceFoundryServiceClient(BaseServiceFoundryServiceClient):
    # TODO (chiragjn): Rename tracking_uri to tfy_host
    def __init__(self, tracking_uri: str, token: Optional[str] = None):
        super().__init__(base_url=tracking_uri)
        self.host_creds = HostCreds(host=self._api_server_url, token=token)

    def get_integration_from_id(self, integration_id: str):
        integration_id = integration_id or ""
        response = http_request_safe(
            host_creds=self.host_creds,
            endpoint=f"{VERSION_PREFIX}/provider-accounts/provider-integrations",
            params={"id": integration_id, "type": "blob-storage"},
            method="get",
            timeout=3,
            max_retries=SERVICEFOUNDRY_CLIENT_MAX_RETRIES,
        )
        data = response.json()
        if (
            data.get("providerIntegrations")
            and len(data["providerIntegrations"]) > 0
            and data["providerIntegrations"][0]
        ):
            return data["providerIntegrations"][0]
        else:
            raise MlFoundryException(
                f"Invalid storage integration id: {integration_id}"
            )
