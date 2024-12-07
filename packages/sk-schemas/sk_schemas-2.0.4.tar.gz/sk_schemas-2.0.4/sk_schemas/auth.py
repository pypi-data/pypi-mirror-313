#!/usr/bin/python3


from pydantic import BaseModel, Field

API_AUTH = "/auth"
API_AUTH_V1 = API_AUTH + "/v1"

API_AUTH_V1_TOKEN = API_AUTH_V1 + "/token"


class OtpUriModel(BaseModel):
    uri: str = Field(description="OTP URI")


class SysSecuritySettings(BaseModel):
    otp_enforce: bool = Field(
        description="OTP Enforcement setting for all users. When set all users must provide OTP for login.",
        default=False,
    )
    token_timeout_sec: int = Field(
        description="Auth Token Timeout in seconds (default: 30 minutes)",
        default=30 * 60,
    )
    password_timeout_sec: int = Field(
        description="Password Timeout in seconds (default: 90 days)", default=86400 * 90
    )
