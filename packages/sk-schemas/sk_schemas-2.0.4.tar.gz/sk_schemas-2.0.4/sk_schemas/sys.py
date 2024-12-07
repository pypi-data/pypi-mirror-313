#!/usr/bin/python3


from enum import Enum
from ipaddress import IPv4Address, IPv6Address
from typing import List, Union

from pydantic import BaseModel, Field

# from pydantic.networks import IPv4Address
from sk_schemas.intf import HostnameModel

API_SYS = "/sys"
API_SYS_V1 = API_SYS + "/v1"


class SwupdateStatusEnum(str, Enum):
    IDLE = "IDLE"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED_SERVER_CHECK = "FAILED_SERVER"
    FAILED_DOWNLOAD = "FAILED_DOWNLOAD"
    FAILED_INSTALL = "FAILED_INSTALL"
    DOWNLOADING = "IMAGE_DOWNLOADING"
    DOWNLOAD_COMPLETE = "IMAGE_DOWNLOAD_COMPLETE"
    INSTALLING = "INSTALLING"
    SUCCESS_NO_UPDATE_AVAILABLE = "SUCCESS_NO_UPDATE"
    REBOOT_REQUIRED = "REBOOT_REQUIRED"


class JobStatusEnum(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class SwupdateStatus(BaseModel):
    status: SwupdateStatusEnum = Field(description="Software Update Status")


class JobNumber(BaseModel):
    id: int = Field(
        description=f"Job Number ID - check {API_SYS_V1}/job-status/<id> for status"
    )
    descritpion: str = Field(description="Description of the Job", default="")


class JobStatus(BaseModel):
    status: JobStatusEnum = Field(description="Job Status")


class SyslogConfigModel(BaseModel):
    enable_remote_syslog: bool = Field(
        description="True if remote syslog server is enabled", default=False
    )
    server_address: IPv4Address | None = Field(
        description="Server IP address", default=None
    )
    server_port: int | None = Field(description="Port", ge=0, le=65535, default=514)
    enable_authentication: bool = Field(
        description="True if authentication is enabled", default=False
    )


class DNSServer(BaseModel):
    ip: Union[IPv4Address, IPv6Address] = Field(description="DNS IP address")
    port: int = Field(description="Port", ge=0, le=65535, default=53)
    domain: HostnameModel | None = Field(description="DNS Domains", default=None)


DEFAULT_DNS_SERVERS: List[DNSServer] = [
    DNSServer(ip=IPv4Address("1.1.1.1")),
    DNSServer(ip=IPv4Address("1.0.0.1")),
    DNSServer(ip=IPv4Address("8.8.8.8")),
    DNSServer(ip=IPv4Address("8.8.4.4")),
    DNSServer(ip=IPv6Address("2606:4700:4700::1111")),
    DNSServer(ip=IPv6Address("2606:4700:4700::1001")),
    DNSServer(ip=IPv6Address("2001:4860:4860::8888")),
    DNSServer(ip=IPv6Address("2001:4860:4860::8844")),
]


class DNSConfigModel(BaseModel):

    servers: List[DNSServer] = Field(
        description="DNS IP address", default=DEFAULT_DNS_SERVERS
    )
    # port: int = Field(description="Port", ge=0, le=65535, default=53)
    # domains: List[HostnameModel] = Field(description="DNS Domains", default=None)
    dnssec: bool = Field(description="True if DNSSEC is enabled", default=False)
    fallback_servers: List[DNSServer] = Field(
        description="Fallback DNS IP address - Default to Goole and Cloudflare",
        default=DEFAULT_DNS_SERVERS,
    )
