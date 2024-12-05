from ipaddress import IPv4Address, IPv6Address
from typing import Union

from pydantic import BaseModel

from tinybird.bi_connector.database import CHBIDatabase


class PlainTextPassword(BaseModel):
    password: str


class CHAllowedIPHosts(BaseModel):
    ip_addresses: list[Union[IPv4Address, IPv6Address]]


class CHBIConnectorUser(BaseModel):
    name: str
    password: PlainTextPassword
    authorized_hosts: CHAllowedIPHosts | None = None
    default_database: CHBIDatabase | None = None
    default_profile: str = "bi_connector"
