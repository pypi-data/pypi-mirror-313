#!/usr/bin/python3


from enum import Enum
from typing import Any, List

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import PydanticCustomError, core_schema

API_CERTS = "/certs"
API_CERTS_V1 = API_CERTS + "/v1"


class HexString(str):
    """Represents a Hex String and provides methods for validation."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:

        return core_schema.with_info_before_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> str:
        """
        Validate a Hex String from the provided str value.

        """
        return cls.validate_hex_string(__input_value)

    @staticmethod
    def validate_hex_string(value: str) -> str:
        """
        Validate a Hex String from the provided byte value.
        """
        if len(value) % 2 != 0:
            raise PydanticCustomError(
                "hex_string_len",
                "Length for a {hex_string} hex string must be even",
                {"hex_string": value},
            )
        # check regex for hex string
        if not all(c in "0123456789abcdefABCDEF" for c in value):
            raise PydanticCustomError(
                "hex_string",
                "Invalid character in {hex_string} hex string",
                {"hex_string": value},
            )
        return value


class CertUsageEnum(str, Enum):
    IPSEC = "ipsec"
    HTTPS_CLIENT = "https_client"
    HTTPS_SERVER = "https_server"
    SYSLOG_CLIENT = "syslog_client"
    SYSLOG_CA = "syslog_ca"


class CertHashEnum(str, Enum):
    SHA_256 = "SHA-256"
    SHA_384 = "SHA-384"
    SHA_512 = "SHA-512"


class CsrSignedRequestModel(BaseModel):
    id: str = Field(description="Unique ID for the CSR")
    fingerprint: str = Field(description="Private Key Fingerprint")
    cert_data: str = Field(description="PEM formatted Public Certificate Data")
    usage: CertUsageEnum = Field(
        description="Certificate Usage",
        default=CertUsageEnum.IPSEC,
    )


class CsrUuidModel(BaseModel):
    id: str = Field(description="Unique ID for the CSR")


class CsrResponseModel(CsrUuidModel):
    fingerprint: str = Field(description="Private Key Fingerprint")
    csr_data: str = Field(description="PEM formatted Certificate Signing Request")


class CertSigningRequestModel(BaseModel):
    alg_type: str = Field(
        description="Private Key Algorithm Type", examples=["RSA", "EC"], default="RSA"
    )
    key_size: int | None = Field(
        description="Key Size for RSA Requests", examples=[4096], default=4096
    )
    curve: str | None = Field(
        description="Curve Name for Elliptic Curve Requests",
        examples=["secp384r1"],
        default="secp384r1",
    )
    hash: CertHashEnum = Field(
        description="Hash Algorithm",
        default=CertHashEnum.SHA_384,
    )

    cn: str = Field(description="Common Name", examples=["user.org"])
    country: str = Field(description="Country Name", examples=["US"])
    locality: str = Field(description="Locality Name", examples=["Los Angeles"])
    organization: str = Field(
        description="Organization Name", examples=["JET Technology Labs Inc."]
    )
    organization_unit: str = Field(
        description="Organizational Unit Name", examples=["Marketing"]
    )
    state: str = Field(description="State Name", examples=["California"])
    dns_names: list[str] = Field(
        description="DNS Name for Subject Alternative Name",
        examples=["user.org"],
        default=[],
    )
    ip_addrs: list[str] = Field(
        description="IP Address for Subject Alternative Name",
        examples=["1.2.3.4"],
        default=[],
    )
    validity_days: int = Field(
        description="Validity in Days", examples=[3650], default=3650
    )


class KeyLoadedInfoModel(BaseModel):
    key_id: HexString | None = Field(
        description="Unique ID for the loaded key (different than KeyInfoModel.fingerprint)",
        default=None,
    )


class KeyFingerprint(BaseModel):
    fingerprint: HexString = Field(description="Unique Fingerprint")


class KeyInfoModel(KeyFingerprint, KeyLoadedInfoModel):
    algorithm: str | None = Field(
        description="Key Algorithm or Curve Name", examples=["RSA", "secp384r1"]
    )


class SharedSecretsModel(BaseModel):
    id: str = Field(
        description="Unique Identifier for Shared Secrets (PPKs, etc.)",
    )
    type: str = Field(
        description="Type of Shared Secret", examples=["PPK", "IKE"], default="PPK"
    )


class SharedSecretDataModel(SharedSecretsModel):
    data: HexString = Field(
        description="Hexadecimal Data String for Shared Secret or Postquantum Preshared Key (PPK, RFC 8784)",
    )


class SSHPubKeyModel(BaseModel):
    data: str = Field(description="SSH Public Key Data")


class CertInfoModel(BaseModel):
    fingerprint: str = Field(description="Unique Fingerprint")
    id: str | None = Field(
        description="Certificate ID", examples=["CN=user.strongswan.org"], default=None
    )
    is_ca: bool | None = Field(
        description="Boolean set ``true`` if certificate is a CA"
    )
    usage: CertUsageEnum = Field(
        description="Certificate Usage",
        default=CertUsageEnum.IPSEC,
    )
    key_fingerprint: str | None = Field(
        description="Private Key Fingerprint", default=None
    )


class x509ExtensionsModel(BaseModel):
    name: str = Field(description="Extension Name")
    critical: bool = Field(description="Extension Critical")
    value: str = Field(description="Extension Value")


class CertDetailModel(BaseModel):
    # x509_details: str = Field(description="PEM formatted X.509 Certificate Information")
    fingerprint: str = Field(description="Unique Fingerprint")
    version: int = Field(
        description="X.509 Version - X.509 v3 (0x2), X.509 v1 (0x0)", examples=[0, 2]
    )
    issuer: str = Field(description=" Certificate Issuer")
    subject: str = Field(description="Certificate Subject")
    serial_number: str = Field(description="Certificate Serial Number")
    not_before: str = Field(description="Certificate Not Before")
    not_after: str = Field(description="Certificate Not After")
    public_key: str = Field(description="Certificate Public Key")
    signature_algorithm: str = Field(description="Certificate Signature Algorithm")
    signature_algorithm_parameters: str | None = Field(
        description="Certificate Signature Algorithm Parameters"
    )
    signature: str = Field(description="Certificate Signature")
    signature_hash_algorithm: str | None = Field(
        description="Certificate Signature Hash Algorithm"
    )
    extensions_count: int = Field(description="Certificate Extensions Count")
    extensions: List[x509ExtensionsModel] = Field(description="Certificate Extensions")


class SSLVerifClientEnum(str, Enum):
    VERIFY_ON = "on"
    VERIFY_OFF = "off"


class TLSConfigModel(BaseModel):
    ssl_verify_client: SSLVerifClientEnum = Field(
        description="Verify Client Certificate (Mutual TLS Authentication)",
        examples=["on", "off"],
        default="off",
    )
    ssl_verify_depth: int = Field(
        description="Maximum Certificate Depth", examples=[1, 2], default=2
    )
