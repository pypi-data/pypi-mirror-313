#!/usr/bin/python3


from pydantic import BaseModel, Field, field_validator

from sk_schemas.certs import SSHPubKeyModel

API_USERS = "/users"
API_USERS_V1 = API_USERS + "/v1"


class UserName(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def check_username(cls, username: str) -> str:
        if len(username) > 32:
            raise ValueError("Username must be at most 32 characters long")

        # check for valid characters
        special_chars = "@-_."
        if not all(c.isalnum() or c in special_chars for c in username):
            valid_chars = f"(only A-Z, a-z, 0-9, {special_chars})"
            raise ValueError("Invalid username must be alphanumeric, " + valid_chars)

        return username


class UserInfo(UserName):
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)
    is_otp_enabled: bool = Field(default=False)


class SSHUserInfo(UserName):
    public_key: SSHPubKeyModel = Field(description="SSH Public Key")
    pass


class UserPassword(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def password_verify(cls, password: str) -> str:
        if len(password) < 14:
            raise ValueError("Password must be at least 14 characters long")
        # spaces are not allowed
        if " " in password:
            raise ValueError("Password cannot contain spaces")
        # check for number, letter and special character
        special_chars = "!@#$%^&*()-+?_=,<>/."
        if (
            not any(char.isdigit() for char in password)
            or not any(char.isalpha() for char in password)
            or not any(char in special_chars for char in password)
        ):
            raise ValueError(
                f"Password must contain at least one number, one letter and one special character ({special_chars})"
            )
        return password


class UserLogin(UserName, UserPassword):
    scope: str = Field(default="")
    client_id: str | None = Field(description="Oauth2 Client ID", default=None)
    client_secret: str | None = Field(
        description="Oauth2 Client Secret (when OTP is enabled this is the OTP)",
        default=None,
    )


class UserChangePassword(UserLogin):
    new_password: UserPassword


class UserCreate(UserInfo, UserPassword):
    pass


class UserUpdate(UserCreate):
    pass
