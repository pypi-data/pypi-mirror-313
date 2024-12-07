import os
from typing import Dict, List, Optional
from urllib.parse import urljoin

from langchain.pydantic_v1 import BaseModel

from truefoundry.deploy.lib.auth.servicefoundry_session import ServiceFoundrySession


class ModelParameters(BaseModel):
    temperature: Optional[float]
    maximum_length: Optional[int]
    top_p: Optional[float]
    top_k: Optional[int]
    repetition_penalty: Optional[float]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]
    stop_sequences: Optional[List[str]]


def validate_tfy_environment(values: Dict):
    gateway_url = values["tfy_llm_gateway_url"] or os.getenv("TFY_LLM_GATEWAY_URL")
    api_key = values["tfy_api_key"] or os.getenv("TFY_API_KEY")

    if gateway_url and api_key:
        values["tfy_llm_gateway_url"] = gateway_url
        values["tfy_api_key"] = api_key
        return values

    sfy_session = ServiceFoundrySession()
    if not sfy_session:
        raise Exception(
            "Unauthenticated: Please login using truefoundry login --host <https://example-domain.com>"
        )

    if not gateway_url:
        gateway_url = urljoin(sfy_session.base_url, "/api/llm")

    if not api_key:
        api_key = sfy_session.access_token

    values["tfy_llm_gateway_url"] = gateway_url
    values["tfy_api_key"] = api_key
    return values
