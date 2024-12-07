from typing import Optional

from truefoundry.pydantic_v1 import BaseModel


class HostCreds(BaseModel):
    host: str
    token: Optional[str] = None
