from __future__ import annotations

import ipaddress
from enum import Enum
from .ip import IpProvider

class Method(Enum):
    GET = 'GET'
    POST = 'POST'


class Socket:
    def __init__(self, ip: str, port: int):
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError("Invalid IP address")

        self.ip = ip
        self.port = port

    def as_addr(self, protocol : str = 'https'):
        return f'{protocol}://{self.ip}:{self.port}'

    @classmethod
    def get_localhost(cls, port : int):
        return cls(ip=IpProvider.get_localhost(),port=port)


class Endpoint:
    def __init__(self, socket : Socket, path : str, method : Method):
        self.path : str = path
        self.method : Method = method
        self.socket : Socket = socket

    def get_url(self, protocol : str = 'https') -> str:
        socket_addr = self.socket.as_addr(protocol=protocol)
        return f'{socket_addr}{self.path}'
