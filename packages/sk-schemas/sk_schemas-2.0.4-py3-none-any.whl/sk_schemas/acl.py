#!/usr/bin/python3


from enum import Enum
from ipaddress import IPv4Network

from pydantic import BaseModel
from sqlalchemy import TypeDecorator
from sqlalchemy.types import Enum as SqlEnum
from sqlalchemy.types import String
from sqlmodel import Column, Field, SQLModel

from sk_schemas.inet import MacAddress
from sk_schemas.intf import IfaceRoleTypes
from sk_schemas.stats import SysTimeModel

API_ACL = "/acl"
API_ACL_V1 = API_ACL + "/v1"


class IPv4NetworkType(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)

    def process_result_value(self, value, dialect):
        return IPv4Network(value)


class AclAction(Enum):
    ACL_ACTION_API_DENY = 0
    ACL_ACTION_API_PERMIT = 1
    ACL_ACTION_API_PERMIT_REFLECT = 2


class IpProtocol(Enum):
    IP_API_PROTO_HOPOPT = 0
    IP_API_PROTO_ICMP = 1
    IP_API_PROTO_IGMP = 2
    IP_API_PROTO_TCP = 6
    IP_API_PROTO_UDP = 17
    IP_API_PROTO_GRE = 47
    IP_API_PROTO_ESP = 50
    IP_API_PROTO_AH = 51
    IP_API_PROTO_ICMP6 = 58
    IP_API_PROTO_EIGRP = 88
    IP_API_PROTO_OSPF = 89
    IP_API_PROTO_SCTP = 132
    IP_API_PROTO_RESERVED = 255


# vl_api_macip_acl_rule_t struct from VPP
class MacIpAclRule(BaseModel):
    """MACIP ACL Rules are ingress only ACL which permit/deny traffic based MAC and IP address matches"""

    is_permit: AclAction = Field(description="Rule Action")
    src_mac: MacAddress = Field(
        description="Source MAC Address",
    )
    src_mac_mask: MacAddress = Field(
        description="Source MAC Address Mask",
    )
    src_prefix: IPv4Network = Field(
        description="Source Prefix",
        sa_column=Column(IPv4NetworkType),
    )
    interface_role: IfaceRoleTypes = Field(
        description="Interface to apply this rule to", default=IfaceRoleTypes.WAN
    )
    priority: int = Field(
        description="Priority in which to apply this rule (highest priority Rules are applied first)",
        ge=0,
        le=4294967295,
        default=0,
    )

    # convert the rule to a string
    def to_string(self) -> str:
        return f"{self.is_permit}-{self.src_mac}-{self.src_mac_mask}-{self.src_prefix}"

    def encode(self) -> dict:
        return {
            "is_permit": self.is_permit.value,
            "src_mac": str(self.src_mac),
            "src_mac_mask": str(self.src_mac_mask),
            "src_prefix": str(self.src_prefix),
        }

    @classmethod
    def from_vapi(cls, vapi_rule, interface_role: IfaceRoleTypes):
        return cls(
            is_permit=vapi_rule.is_permit,
            src_prefix=IPv4Network(str(vapi_rule.src_prefix)),
            src_mac=MacAddress(vapi_rule.src_mac),
            src_mac_mask=MacAddress(vapi_rule.src_mac_mask),
            interface_role=interface_role,
        )

    def __eq__(self, other):
        if not isinstance(other, MacIpAclRule):
            return False
        # don't compare priority (this is only used for sorting)
        a = self.model_dump()
        a.pop("priority", None)
        b = other.model_dump()
        b.pop("priority", None)
        return a == b


# vl_api_acl_rule_t struct from VPP
class IpAclRule(SQLModel):
    """ACL IP Rules permit traffic based on a number of Layer3/Layer4 fields"""

    is_permit: AclAction = Field(
        description="Rule Action",
        sa_column=Column(SqlEnum(AclAction)),
    )
    src_prefix: IPv4Network = Field(
        description="Source Prefix",
        sa_column=Column(IPv4NetworkType),
    )
    dst_prefix: IPv4Network = Field(
        description="Source Prefix",
        sa_column=Column(IPv4NetworkType),
    )
    proto: int = Field(
        description="Protocol",
        ge=0,
        le=255,
    )
    src_port_first: int = Field(
        description="Source Port First", ge=0, le=65535, default=0
    )
    src_port_last: int = Field(
        description="Source Port Last", ge=0, le=65535, default=0
    )
    dst_port_first: int = Field(
        description="Destination Port First", ge=0, le=65535, default=0
    )
    dst_port_last: int = Field(
        description="Destination Port Last", ge=0, le=65535, default=0
    )
    tcp_flags_mask: int = Field(description="TCP Flags", ge=0, le=255, default=0)
    tcp_flags_value: int = Field(description="TCP Flags", ge=0, le=255, default=0)
    is_input: bool = Field(description="Input or Output")
    interface_role: IfaceRoleTypes = Field(
        description="Interface to apply this rule to",
        default=IfaceRoleTypes.WAN,
        sa_column=Column(SqlEnum(IfaceRoleTypes)),
    )
    priority: int = Field(
        description="Priority in which to apply this rule (highest priority Rules are applied first)",
        ge=0,
        le=4294967295,
        default=0,
    )

    def __eq__(self, other):
        if not isinstance(other, IpAclRule):
            return False
        # don't compare priority (this is only used for sorting)
        a = self.model_dump()
        a.pop("priority", None)
        b = other.model_dump()
        b.pop("priority", None)
        return a == b

    # create new instance from raw data
    @classmethod
    def from_vapi(cls, vapi_rule, is_input: bool, interface_role: IfaceRoleTypes):
        return cls(
            is_permit=vapi_rule.is_permit,
            src_prefix=vapi_rule.src_prefix,
            dst_prefix=vapi_rule.dst_prefix,
            proto=vapi_rule.proto,
            src_port_first=vapi_rule.srcport_or_icmptype_first,
            src_port_last=vapi_rule.srcport_or_icmptype_last,
            dst_port_first=vapi_rule.dstport_or_icmpcode_first,
            dst_port_last=vapi_rule.dstport_or_icmpcode_last,
            tcp_flags_mask=vapi_rule.tcp_flags_mask,
            tcp_flags_value=vapi_rule.tcp_flags_value,
            is_input=is_input,
            interface_role=interface_role,
        )

    # convert the rule to a string
    def to_string(self) -> str:
        in_out_str = "In" if self.is_input else "Out"
        return f"{self.is_permit.value}-{in_out_str}-{self.src_port_last}-{self.src_port_first}-{self.dst_port_last}-{self.dst_port_first}-{self.proto}-{self.src_prefix}-{self.dst_prefix}-{self.tcp_flags_mask}-{self.tcp_flags_value}"

    def encode(self) -> dict:
        return {
            "is_permit": self.is_permit.value,
            "proto": self.proto,
            "srcport_or_icmptype_first": self.src_port_first,
            "srcport_or_icmptype_last": self.src_port_last,
            "src_prefix": str(self.src_prefix),
            "dstport_or_icmpcode_first": self.dst_port_first,
            "dstport_or_icmpcode_last": self.dst_port_last,
            "dst_prefix": str(self.dst_prefix),
        }


class AclStats(SysTimeModel):

    rule_description: str = Field(
        description="ACL Rule Tag Description",
    )
    packets: int = Field(
        description="Packets Filtered by ACL",
    )
    bytes: int = Field(
        description="Bytes Filtered by ACL",
    )
