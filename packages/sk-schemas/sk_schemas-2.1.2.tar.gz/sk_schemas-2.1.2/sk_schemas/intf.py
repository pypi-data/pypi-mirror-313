#!/usr/bin/python3


import re
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from sk_schemas.inet import IpSubnetModel

API_INTERFACES = "/interfaces"
API_INTERFACES_V1 = API_INTERFACES + "/v1"
API_INTERFACES_V2 = API_INTERFACES + "/v2"

VPP_MAC_ADDR_FIELD = Field(
    description="Interface MAC Address",
    examples=["00:11:22:33:44:55"],
    json_schema_extra={"vpp_api": "l2_address"},
)


class IfaceRoleTypes(str, Enum):
    WAN = "wan"
    LAN = "lan"
    MGMT = "mgmt"


class HostnameModel(BaseModel):
    hostname: str = Field(
        description="Hostname ",
        examples=["hostname"],
    )

    @field_validator("hostname")
    @classmethod
    def check_hostname(cls, hostname: str) -> str:
        if len(hostname) > 255:
            raise ValueError("Invalid Hostname - too long")

        if hostname[-1] == ".":
            # strip exactly one dot from the right, if present
            hostname = hostname[:-1]

        allowed = re.compile("(?!-)[A-Z0-9-]{1,63}(?<!-)$", re.IGNORECASE)
        if not all(allowed.match(x) for x in hostname.split(".")):
            raise ValueError("Invalid Hostname")

        return hostname


class VppIfIndex(BaseModel):
    sw_if_index: int = Field(
        description="Interface Index",
        examples=[0],
        json_schema_extra={"vpp_api": "sw_if_index"},
    )


class VppIfaceSettings(VppIfIndex):
    if_name: str = Field(
        description="Interface Name",
        examples=["eth0"],
        json_schema_extra={"vpp_api": "interface_name"},
    )

    if_type: str = Field(
        description="Interface Type",
        examples=["IF_API_TYPE_HARDWARE", "IF_API_TYPE_P2P", "IF_API_TYPE_SUBIF"],
        json_schema_extra={"vpp_api": "type"},
    )
    mac_addr: str = VPP_MAC_ADDR_FIELD

    flags: str = Field(
        description="Interface Flags",
        examples=[
            "IF_STATUS_API_FLAG_LINK_UP",
        ],
        json_schema_extra={"vpp_api": "flags"},
    )

    link_duplex: str = Field(
        description="Link Duplex",
        examples=["LINK_DUPLEX_API_FULL", "LINK_DUPLEX_API_HALF"],
        json_schema_extra={"vpp_api": "link_duplex"},
    )

    link_speed: int = Field(
        ge=0,
        description="Link Speed",
        examples=[1000],
        json_schema_extra={"vpp_api": "link_speed"},
    )

    link_mtu: int = Field(
        ge=0,
        description="Link MTU",
        examples=[1500],
        json_schema_extra={"vpp_api": "link_mtu"},
    )

    sub_id: int = Field(
        description="A number 0-N to uniquely identify this subif on super if",
        examples=[1],
        json_schema_extra={"vpp_api": "sub_id"},
    )

    sub_number_of_tags: int = Field(
        description="Number of tags (0 - 2)",
        examples=[0],
        json_schema_extra={"vpp_api": "sub_number_of_tags"},
    )

    vlanid: int = Field(
        description="VLAN ID", examples=[100], json_schema_extra={"vpp_api": "b_vlanid"}
    )


class IfaceSettings(VppIfaceSettings):
    ip_addrs: list[IpSubnetModel] = Field(
        description="Interface IP Addresses",
        default=[],
    )
    interface_role: IfaceRoleTypes = Field(description="Interface Role")


class IfaceRoleSet(BaseModel):
    wan_mac_addr: str = VPP_MAC_ADDR_FIELD
    lan_mac_addr: str = VPP_MAC_ADDR_FIELD
