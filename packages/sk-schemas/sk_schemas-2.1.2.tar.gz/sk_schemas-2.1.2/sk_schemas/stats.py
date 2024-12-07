#!/usr/bin/python3

from enum import Enum
from typing import List

from pydantic import BaseModel, Field

API_STATS = "/stats"
API_STATS_V1 = API_STATS + "/v1"
API_STATS_V2 = API_STATS + "/v2"


class SysTimeModel(BaseModel):
    time: str = Field(
        description="System Time ISO formatted",
        examples=["2021-01-01T00:00:00+00:00"],
    )


class StatsStringModel(BaseModel):
    stats: str = Field(description="Statistics string")


class NameValue(BaseModel):
    name: str = Field(description="Name")
    value: int = Field(description="Value", examples=[1000])


class DpStats(SysTimeModel):
    stats: List[NameValue] = Field(description="Statistics List")


class StatusEnum(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    CONFIGURING = "CONFIGURING"
    RESTARTING = "RESTARTING"
    UNKNOWN = "UNKNOWN"


class ComponentEnum(str, Enum):
    vpp = "vpp"
    charon = "charon"
    ssh = "ssh"
    SecureKeyDataplane = "SecureKey-dataplane"
    https = "https"


class StatusModel(BaseModel):
    component: ComponentEnum = Field(description="Component Name")
    status: StatusEnum = Field(description="Status")


class FileDataModel(BaseModel):
    file_name: str = Field(description="Filename")
    data: bytes = Field(description="File Data")


class MachineIDModel(BaseModel):
    machine_id: str = Field(
        description="Machine ID for this device",
        examples=["089a2ff00dd9476ffd7ff2aaabc34ed89"],
    )


class SwVersionModel(BaseModel):
    name: str = Field(
        description="Software Application Name",
        examples=["sk_vpn"],
    )
    version: str = Field(
        description="Version",
        examples=["1.0-12345678"],
    )


class SystemVersionModel(BaseModel):
    software: List[SwVersionModel] = Field(
        description="Software Application Versions",
    )


class SystemReportModel(BaseModel):
    name: str = Field(
        description="Software Component Name",
        examples=["Secure Boot", "cpuinfo", "meminfo"],
    )
    data: str = Field(
        description="Report data",
        examples=["Enabled", "Disabled", "Not Available"],
    )
