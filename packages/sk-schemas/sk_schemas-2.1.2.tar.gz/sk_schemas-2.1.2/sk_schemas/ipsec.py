#!/usr/bin/python3


from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from sk_schemas.inet import IPorDNSNameModel, IpSubnetModel

API_IPSEC = "/ipsec"
API_IPSEC_V1 = API_IPSEC + "/v1"


class NameModel(BaseModel):
    name: str = Field(
        description="Name Field ",
        examples=["string_name-123"],
        pattern="^[-_()0-9a-zA-Z]+$",
    )


class ConnectionSaModel(BaseModel):
    connection_name: NameModel
    sa_name: NameModel


class ModeEnum(str, Enum):
    transport = "transport"
    tunnel = "tunnel"


class StartActionEnum(str, Enum):
    start = "start"
    none = "none"
    trap = "trap"
    trap_start = "trap-start"


class EspEncapEnum(str, Enum):
    espintcp = "espintcp"
    espinudp = "espinudp"
    none = "none"


class IpsecLifetimeEnum(str, Enum):
    terminate_clear = "terminate_clear"
    terminate_hold = "terminate_hold"
    replace_val = "replace"


class IpsecTrafficDirEnum(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class IpsecSpdActionEnum(str, Enum):
    protect = "protect"
    bypass = "bypass"
    discard = "discard"


class LifetimeTimeModel(BaseModel):
    time: int = Field(
        description="""Time in seconds since the IPsec SA was added.
            For example, if this value is 180 seconds, it
            means the IPsec SA expires in 180 seconds since
            it was added.  The value 0 implies infinite.""",
        ge=0,
        le=4294967295,
        default=[0],
    )


class LifetimeBytesModel(BaseModel):
    bytes: int = Field(
        description="""If the IPsec SA processes the number of bytes
            expressed in this leaf, the IPsec SA expires and
            SHOULD be rekeyed.  The value 0 implies
            infinite.""",
        ge=0,
        le=9223372036854775807,
        default=[0],
    )


class LifetimePacketsModel(BaseModel):
    packets: int = Field(
        description="""If the IPsec SA processes the number of packets
            expressed in this leaf, the IPsec SA expires and
            SHOULD be rekeyed.  The value 0 implies
            infinite.""",
        ge=0,
        le=4294967295,
        default=[0],
    )


class LifetimeIdleModel(BaseModel):
    idle: int = Field(
        description="""When an NSF stores an IPsec SA, it
            consumes system resources.  For an idle IPsec SA, this
            is a waste of resources.  If the IPsec SA is idle
            during this number of seconds, the IPsec SA
            SHOULD be removed.  The value 0 implies
            infinite.""",
        ge=0,
        le=4294967295,
        default=[0],
    )


class SACertModel(BaseModel):
    id: str = Field(description="Identifier", examples=["CN=user.strongswan.org"])
    class_: str = Field(description="Class Name for the SA", examples=["public key"])
    groups: List[str] = Field(description="Groups", default=[""])
    cert_policy: List[str] = Field(description="Certificate Policy", default=[""])
    certs: List[str] = Field(description="Certificates List", default=[""])
    cacerts: List[str] = Field(description="CA Certificates List", default=[""])


class ChildConnModel(BaseModel, extra="allow"):
    name: str = Field(description="Child SA Name", examples=["net1-net2"])
    mode: str = Field(description="Tunnel or Transport Mode", examples=["TUNNEL"])
    rekey_time: int = Field(description="Re-Key Seconds")
    rekey_bytes: int = Field(description="Re-Key Bytes")
    rekey_packets: int = Field(description="Re-Key Packets")
    dpd_action: str = Field(description="DPD Action")
    close_action: str = Field(description="Close Action")
    local_ts: List[IpSubnetModel] = Field(description="Local Traffic Selectors")
    remote_ts: List[IpSubnetModel] = Field(description="Remote Traffic Selectors")


class ConnectionModel(BaseModel, extra="allow"):
    name: str = Field(description="IPsec Connection Name", examples=["Connection-1"])
    local_addrs: List[IPorDNSNameModel] = Field(description="Local Addressess")
    remote_addrs: List[IPorDNSNameModel] = Field(description="Remote Addressess")
    version: str = Field(description="IKEv1/2 Version")
    reauth_time: int = Field(description="Re-Authentication Time in Seconds", default=0)
    rekey_time: int = Field(description="Re-Key Time in Seconds")
    unique: str = Field(description="Unique name for this Connection")
    ppk_id: str | None = Field(
        description="Postquantum Preshared Key Identifier (PPK)", default=None
    )
    ppk_required: str | None = Field(description="Is PPK required", default=None)
    local_1: List[SACertModel] = Field(description="List of Local SAs")
    remote_1: List[SACertModel] = Field(description="List of Remote SAs")
    children: List[ChildConnModel] = Field(description="List of Children SAs")


class EncParamsModel(BaseModel):
    encr_alg: str = Field(
        description="Encryption Algorithm",
        examples=["AES_GCM_16"],
        default="AES_GCM_16",
        json_schema_extra={"key": "encr-alg"},
    )
    encr_keysize: int = Field(
        description="Encryption Key size in Bits",
        examples=[256],
        default=256,
        json_schema_extra={"key": "encr-keysize"},
    )
    dh_group: str = Field(
        description="DH Group Name",
        examples=["MODP_4096", "ECP_384"],
        default="",
        json_schema_extra={"key": "dh-group"},
    )
    kem_groups: List[str] | None = Field(
        description="Additional Key Exchange Methods (RFC 9370)",
        examples=["mlkem786", "mlkem1024"],
        default=None,
        max_length=7,
    )


class ChildConnCreateModel(EncParamsModel, NameModel):
    mode: str = Field(
        description="Tunnel or Transport Mode", examples=["TUNNEL"], default="TUNNEL"
    )
    protocol: str = Field(description="Protocol Name", examples=["ESP"], default="ESP")
    rekey_time: int = Field(
        description="Rekey Time Seconds",
        examples=[6000],
        default=3600,
        json_schema_extra={"key": "rekey-time"},
    )
    life_time: int = Field(
        description="Life Time Seconds",
        examples=[6000],
        default=6000,
        json_schema_extra={"key": " life-time"},
    )
    esn: bool = Field(description="Extended Sequence Number", default=False)
    start_action: StartActionEnum = Field(
        description="Start Action",
        default=StartActionEnum.none,
        json_schema_extra={"key": "start-action"},
    )
    local_ts: List[IpSubnetModel] = Field(
        description="Local Traffic Selectors", json_schema_extra={"key": " local-ts"}
    )
    remote_ts: List[IpSubnetModel] = Field(
        description="Remote Traffic Selectors", json_schema_extra={"key": " remote-ts"}
    )


class ChildSAModel(ChildConnCreateModel, extra="allow"):
    uniqueid: str = Field(description="Unique ID for this SA")
    reqid: str = Field(description="Req ID for this SA")
    state: str = Field(description="State of this SA", examples=["ESTABLISHED"])
    spi_in: str = Field(
        description="Input SPI Value hex string",
        examples=["17c06cc2fc722e8a"],
        json_schema_extra={"key": " spi-in"},
    )
    spi_out: str = Field(
        description="Output SPI Value hex string",
        examples=["17c06cc2fc722e8a"],
        json_schema_extra={"key": " spi-out"},
    )
    bytes_in: int = Field(
        description="Bytes Input",
        examples=[1000],
        json_schema_extra={"key": " bytes-in"},
    )
    packets_in: int = Field(
        description="Packets Input",
        examples=[1000],
        json_schema_extra={"key": " packets-in"},
    )
    bytes_out: int = Field(
        description="Bytes Output",
        examples=[1000],
        json_schema_extra={"key": " bytes-out"},
    )
    packets_out: int = Field(
        description="Packets Output",
        examples=[1000],
        json_schema_extra={"key": " packets-out"},
    )
    install_time: int = Field(
        description="Install Time Seconds",
        examples=[6000],
        json_schema_extra={"key": " install-time"},
    )
    encap: bool = Field(
        description="True if UDP Encapslation (NAT Traversal) is enabled", default=False
    )


class BaseIKEConnModel(EncParamsModel, NameModel):
    version: int = Field(
        description="IKEv1/2 Version integer", examples=[1, 2], default=2
    )
    local_host: IPorDNSNameModel = Field(
        description="Local IP Address", json_schema_extra={"key": " local-host"}
    )
    local_port: int = Field(
        description="Local Port Number",
        ge=0,
        le=65535,
        examples=[4500],
        default=4500,
        json_schema_extra={"key": " local-port"},
    )
    local_id: str = Field(
        description="Local Certificate ID",
        examples=["CN=user1.strongswan.org"],
        json_schema_extra={"key": " local-id"},
    )
    local_cert_fingerprint: str | None = Field(
        description="Local Certificate Fingerprint",
        default=None,
    )
    local_cacerts: List[str] = Field(
        description="Local CA Certificate IDs",
        examples=["CN=CA1.strongswan.org"],
        json_schema_extra={"key": "local-cacert"},
        default=[],
    )
    remote_host: IPorDNSNameModel = Field(
        description="Remote IP Address", json_schema_extra={"key": " remote-host"}
    )
    remote_port: int = Field(
        description="Remote Port Number",
        ge=0,
        le=65535,
        examples=[4500],
        default=4500,
        json_schema_extra={"key": " remote-port"},
    )
    remote_id: str = Field(
        description="Remote Certificate ID",
        examples=["CN=user2.strongswan.org"],
        json_schema_extra={"key": " remote-id"},
    )
    remote_cacerts: List[str] = Field(
        description="Remote CA Certificate IDs",
        examples=["CN=CA2.strongswan.org"],
        json_schema_extra={"key": "cacert"},
        default=[],
    )
    prf_alg: str = Field(
        description="Pseudo Random Function",
        examples=["PRF_HMAC_SHA2_384"],
        default="PRF_HMAC_SHA2_384",
        json_schema_extra={"key": " prf-alg"},
    )
    rekey_time: int = Field(
        description="Rekey Interval in seconds, Default=4 hours, Disabled=0",
        examples=[6000],
        default=60 * 60 * 4,
        json_schema_extra={"key": " rekey-time"},
    )
    reauth_time: int = Field(
        description="IKE Reauthentication Interval in seconds, Default=0, Disabled=0",
        examples=[3600],
        default=0,
        json_schema_extra={"key": " reauth-time"},
    )
    ppk_id: str | None = Field(
        description="Postquantum Preshared Key Identifier (PPK, RFC 8784)",
        default=None,
        json_schema_extra={"key": " ppk_id"},
    )


class ConnCreateModel(BaseIKEConnModel, EncParamsModel, NameModel):
    child_sas: List[ChildConnCreateModel] = Field(
        description="Child SAs", json_schema_extra={"key": " child-sas"}
    )


class SAModel(BaseIKEConnModel, extra="allow"):
    uniqueid: str = Field(description="Unique ID for this SA")
    state: str = Field(description="State of this SA", examples=["ESTABLISHED"])
    initiator: str = Field(
        description="Indicates if this is the initiator",
        examples=["yes"],
        default="no",
    )
    initiator_spi: str = Field(
        description="Initiator's SPI Value hex string",
        examples=["17c06cc2fc722e8a"],
        json_schema_extra={"key": " initiator-spi"},
    )
    responder_spi: str = Field(
        description="Responder's SPI Value hex string",
        examples=["27c06cc2fc722e8a"],
        json_schema_extra={"key": " responder-spi"},
    )
    established: int = Field(
        description="Established time in seconds", examples=[60], default=0
    )
    child_sas: List[ChildSAModel] = Field(
        description="Child SAs", json_schema_extra={"key": " child-sas"}
    )
    nat_remote: str = Field(
        description="Network Address Translation Remote setting",
        examples=["yes", "no"],
        json_schema_extra={"key": "nat-remote"},
        default="no",
    )
    nat_any: str = Field(
        description="Network Address Translation Any setting",
        examples=["yes", "no"],
        json_schema_extra={"key": "nat-any"},
        default="no",
    )
    tasks_passive: List[str] = Field(
        description="Tasks Passive",
        examples=[["IKE_INIT", "IKE_CERT_PRE", "IKE_AUTH"]],
        json_schema_extra={"key": "tasks-passive"},
        default=[],
    )
    tasks_active: List[str] | None = Field(description="Tasks Active", default=[])

    tasks_queued: List[str] = Field(
        description="List of currently queued tasks for execution",
        examples=[["CHILD_CREATE"]],
        json_schema_extra={"key": "tasks-queued"},
        default=[],
    )
