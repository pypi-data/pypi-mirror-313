import time
from enum import Enum
from typing import Optional

import jwt
from typing_extensions import NotRequired, TypedDict

from truefoundry.pydantic_v1 import BaseModel, Field, NonEmptyStr, validator


class UserType(Enum):
    user = "user"
    serviceaccount = "serviceaccount"


class UserInfo(BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    user_id: NonEmptyStr
    user_type: UserType = UserType.user
    email: Optional[str] = None
    tenant_name: NonEmptyStr = Field(alias="tenantName")


class _DecodedToken(TypedDict):
    tenantName: str
    exp: int
    username: str
    email: NotRequired[str]
    userType: UserType


class Token(BaseModel):
    access_token: NonEmptyStr = Field(alias="accessToken", repr=False)
    refresh_token: Optional[NonEmptyStr] = Field(alias="refreshToken", repr=False)
    decoded_value: Optional[_DecodedToken] = Field(exclude=True, repr=False)

    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    @validator("decoded_value", always=True, pre=True)
    def _decode_jwt(cls, v, values, **kwargs) -> _DecodedToken:
        access_token = values["access_token"]
        return jwt.decode(
            access_token,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_exp": False,
            },
        )

    @property
    def tenant_name(self) -> str:
        return self.decoded_value["tenantName"]

    def is_going_to_be_expired(self, buffer_in_seconds: int = 120) -> bool:
        exp = int(self.decoded_value["exp"])
        return (exp - time.time()) < buffer_in_seconds

    def to_user_info(self) -> UserInfo:
        return UserInfo(  # type: ignore[call-arg]
            user_id=self.decoded_value["username"],
            email=self.decoded_value["email"]
            if "email" in self.decoded_value
            else None,
            user_type=UserType(self.decoded_value.get("userType", UserType.user.value)),
            tenant_name=self.tenant_name,
        )


class CredentialsFileContent(BaseModel):
    class Config:
        allow_mutation = False

    access_token: NonEmptyStr = Field(repr=False)
    refresh_token: Optional[NonEmptyStr] = Field(repr=False)
    host: NonEmptyStr

    def to_token(self) -> Token:
        return Token(  # type: ignore[call-arg]
            access_token=self.access_token, refresh_token=self.refresh_token
        )


class TenantInfo(BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    tenant_name: NonEmptyStr = Field(alias="tenantName")
    auth_server_url: str


class PythonSDKConfig(BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    min_version: str = Field(alias="minVersion")
    truefoundry_cli_min_version: str = Field(alias="truefoundryCliMinVersion")
    use_sfy_server_auth_apis: Optional[bool] = Field(
        alias="useSFYServerAuthAPIs", default=False
    )


class DeviceCode(BaseModel):
    class Config:
        allow_population_by_field_name = True
        allow_mutation = False

    user_code: str = Field(alias="userCode")
    device_code: str = Field(alias="deviceCode")
    verification_url: Optional[str] = Field(alias="verificationURI")
    complete_verification_url: Optional[str] = Field(alias="verificationURIComplete")
    expires_in_seconds: int = Field(alias="expiresInSeconds", default=60)
    interval_in_seconds: int = Field(alias="intervalInSeconds", default=1)
    message: Optional[str] = Field(alias="message")

    def get_user_clickable_url(self, auth_host: str) -> str:
        return f"{auth_host}/authorize/device?userCode={self.user_code}"
