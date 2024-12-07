#!/usr/bin/python3


from sqlmodel import Field, SQLModel

API_CRYPTO = "/crypto"
API_CRYPTO_V1 = API_CRYPTO + "/v1"


class CryptoSettings(SQLModel):
    async_enabled: bool = Field(
        description="True if Async Crypto is enabled", default=True
    )
    secure_key_enabled: bool = Field(
        description="True if Secure Key Crypto Engine is enabled. Changing this setting requires a reboot",
        default=True,
    )
