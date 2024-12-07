#!/usr/bin/python3


import re
from typing import Any, Union

from pydantic import (
    BaseModel,
    Field,
    GetCoreSchemaHandler,
    IPvAnyInterface,
    field_validator,
)
from pydantic.networks import IPvAnyAddress
from pydantic_core import PydanticCustomError, core_schema

# from pydantic_extra_types.mac_address import MacAddress  # type: ignore


class TcpUdpPortModel(BaseModel):
    port: int = Field(description="Port", ge=0, le=65535)


class IpModel(BaseModel):
    ip: IPvAnyAddress = Field(
        description="IPv4 or IPv6 Address",
        examples=["237.84.2.178", "5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b"],
    )


class IPorDNSNameModel(BaseModel):
    host: Union[IPvAnyAddress, str] = Field(
        union_mode="smart",
        description="IPv4, IPv6 Address or DNS Host Name (RFC 2181 compliant)",
        examples=[
            "237.84.2.178",
            "5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b",
            "test.example.com",
            "%any",
        ],
    )

    @field_validator("host")
    @classmethod
    def check_host(cls, host: Union[IPvAnyAddress, str]) -> Union[IPvAnyAddress, str]:
        try:
            ip_any = IPvAnyAddress(host)
            return ip_any  # type: ignore
        except ValueError:
            if not isinstance(host, str):
                raise ValueError("Invalid DNS host name")
            pass

        if len(host) > 255:
            raise ValueError("Invalid DNS Hostname - too long")

        if host[-1] == ".":
            # strip exactly one dot from the right, if present
            host = host[:-1]

        allowed = re.compile("(?!-)[a-zA-Z0-9-]{1,63}(?<!-)$")
        if not all(allowed.match(x) for x in host.split(".")):
            # special case for %any
            if host != "%any":
                raise ValueError("Invalid DNS host name")

        # while not strictly required this helps weed out bad IPv4 addresses - at least one letter must appear
        if not any(c.isalpha() for c in host):
            raise ValueError("Invalid DNS host name - at least one letter required")

        return host


class IpSubnetModel(BaseModel):
    subnet: IPvAnyInterface = Field(
        description="IPv4 or IPv6 Subnet",
        examples=["237.84.2.178/24", "5be8:dde9:7f0b:d5a7:bd01:b3be:9c69:573b/64"],
    )


class RouteModel(BaseModel):
    # model_config = ConfigDict(from_attributes=True)

    ip_subnet: IpSubnetModel
    gateway_ip: IpModel | None
    if_name: str | None = Field(
        description="Interface Name",
        examples=["eth0"],
    )


class MacAddress(str):
    """Represents a MAC address and provides methods for conversion, validation, and serialization.

    ```py

    class Network(BaseModel):
        mac_address: MacAddress

    network = Network(mac_address="00:00:5e:00:53:01")
    print(network)
    #> mac_address='00:00:5e:00:53:01'
    ```
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        """
        Return a Pydantic CoreSchema with the MAC address validation.

        Args:
            source: The source type to be converted.
            handler: The handler to get the CoreSchema.

        Returns:
            A Pydantic CoreSchema with the MAC address validation.

        """
        return core_schema.with_info_before_validator_function(
            cls._validate,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate(cls, __input_value: str, _: Any) -> str:
        """
        Validate a MAC Address from the provided str value.

        Args:
            __input_value: The str value to be validated.
            _: The source type to be converted.

        Returns:
            str: The parsed MAC address.

        """
        return cls.validate_mac_address(__input_value.encode())

    @staticmethod
    def validate_mac_address(value: bytes) -> str:
        """
        Validate a MAC Address from the provided byte value.
        """
        if len(value) < 14:
            raise PydanticCustomError(
                "mac_address_len",
                "Length for a {mac_address} MAC address must be {required_length}",
                {"mac_address": value.decode(), "required_length": 14},
            )

        if value[2] in [ord(":"), ord("-")]:
            if (len(value) + 1) % 3 != 0:
                raise PydanticCustomError(
                    "mac_address_format",
                    "Must have the format xx:xx:xx:xx:xx:xx or xx-xx-xx-xx-xx-xx",
                )
            n = (len(value) + 1) // 3
            if n not in (6, 8, 20):
                raise PydanticCustomError(
                    "mac_address_format",
                    "Length for a {mac_address} MAC address must be {required_length}",
                    {"mac_address": value.decode(), "required_length": (6, 8, 20)},
                )
            mac_address = bytearray(n)
            x = 0
            for i in range(n):
                try:
                    byte_value = int(value[x : x + 2], 16)
                    mac_address[i] = byte_value
                    x += 3
                except ValueError as e:
                    raise PydanticCustomError(
                        "mac_address_format", "Unrecognized format"
                    ) from e

        elif value[4] == ord("."):
            if (len(value) + 1) % 5 != 0:
                raise PydanticCustomError(
                    "mac_address_format", "Must have the format xx.xx.xx.xx.xx.xx"
                )
            n = 2 * (len(value) + 1) // 5
            if n not in (6, 8, 20):
                raise PydanticCustomError(
                    "mac_address_format",
                    "Length for a {mac_address} MAC address must be {required_length}",
                    {"mac_address": value.decode(), "required_length": (6, 8, 20)},
                )
            mac_address = bytearray(n)
            x = 0
            for i in range(0, n, 2):
                try:
                    byte_value = int(value[x : x + 2], 16)
                    mac_address[i] = byte_value
                    byte_value = int(value[x + 2 : x + 4], 16)
                    mac_address[i + 1] = byte_value
                    x += 5
                except ValueError as e:
                    raise PydanticCustomError(
                        "mac_address_format", "Unrecognized format"
                    ) from e

        else:
            raise PydanticCustomError("mac_address_format", "Unrecognized format")

        return ":".join(f"{b:02x}" for b in mac_address)


class MacAddressModel(BaseModel):
    mac_addr: MacAddress


class IfAddrModel(MacAddressModel):
    ip_subnet: IpSubnetModel
