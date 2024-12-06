from __future__ import annotations
from typing import Optional

class Adapter:

    @classmethod
    def from_nmcli_output(cls,section: str) -> Adapter:
        the_adapter = Adapter()
        for line in section.split('\n'):
            if ':' not in line:
                continue
            key, value = line.split(':', 1)
            value = value.strip()

            if key == "GENERAL.DEVICE":
                the_adapter.name = value
            elif key == "GENERAL.TYPE":
                the_adapter.adapter_type = value
            elif key == "IP4.ADDRESS[1]":
                the_adapter.ipv4_address = value.split('/')[0]
                the_adapter.subnet_mask = value.split('/')[1] if '/' in value else None
            elif key == "IP4.GATEWAY":
                the_adapter.default_gateway = value
            elif key == "IP6.ADDRESS[1]":
                the_adapter.ipv6_address = value.split('/')[0]
            elif key == "IP4.DOMAIN[1]":
                the_adapter.dns_suffix = value

        return the_adapter

    def __init__(
        self,
        technical_name: Optional[str] = None,
        adapter_type: Optional[str] = None,
        dns_suffix: Optional[str] = None,
        ipv4_address: Optional[str] = None,
        ipv6_address: Optional[str] = None,
        subnet_mask: Optional[str] = None,
        default_gateway: Optional[str] = None
    ) -> None:
        self.name: Optional[str] = technical_name
        self.adapter_type: Optional[str] = adapter_type
        self.dns_suffix: Optional[str] = dns_suffix
        self.ipv4_address: Optional[str] = ipv4_address
        self.ipv6_address: Optional[str] = ipv6_address
        self.subnet_mask: Optional[str] = subnet_mask
        self.default_gateway: Optional[str] = default_gateway

    def __str__(self):
        indent = 2 * ' '
        formatted_info = [
            self.get_heading(),
            '',
            f'{indent}{self.get_interface_type()}' if self.name is not None else '',
            f'{indent}{self.get_dns_suffix()}' if self.dns_suffix is not None else '',
            f'{indent}{self.get_ipv4_addr()}' if self.ipv4_address is not None else '',
            f'{indent}{self.get_ipv6_addr()}' if self.ipv6_address is not None else '',
            f'{indent}{self.get_subnet_mask()}' if self.subnet_mask is not None else '',
            f'{indent}{self.get_formatted_default_gateway()}' if self.default_gateway is not None else ''
        ]


        non_empty_info = filter(lambda x: x != '', formatted_info)

        return "\n".join(non_empty_info)

    def get_heading(self):
        friendly_name = self.get_friendly_interface_name(self.name)
        return friendly_name

    def get_interface_type(self):
        return f"{self.get_formatted_label('Type')}{self.adapter_type}"

    def get_dns_suffix(self):
        return f"{self.get_formatted_label('DNS Suffix')}{self.dns_suffix}"

    def get_ipv4_addr(self):
        return f"{self.get_formatted_label('IPv4 Address')}{self.ipv4_address}"

    def get_ipv6_addr(self):
        return f"{self.get_formatted_label('IPv6 Address')}{self.ipv6_address}"

    def get_subnet_mask(self):
        try:
            the_int = int(self.subnet_mask)
            self.subnet_mask = self.cidr_to_netmask(the_int)
        except:
            return ''
        return f"{self.get_formatted_label('Subnet Mask')}{self.subnet_mask}"

    def get_formatted_default_gateway(self):
        return f"{self.get_formatted_label('Default Gateway')}{self.default_gateway}"


    @staticmethod
    def get_formatted_label(label):
        target_size = 30
        blank_padding = " " * (target_size - len(label))
        dotted_padding = ''.join([c if (i+len(label)) % 2 == 0 else '.' for i, c in enumerate(blank_padding)])
        adjusted_label = f"{label}{dotted_padding}"[:target_size] + " : "
        return adjusted_label

    @staticmethod
    def get_friendly_interface_name(interface_name : str) -> str:
        if interface_name.startswith('en'):
            return "Ethernet Adapter"
        elif interface_name.startswith('wl'):
            return "Wireless LAN Adapter"
        elif interface_name.startswith('virbr'):
            return "Virtual Bridge Interface"
        elif interface_name.startswith('veth'):
            return "Virtual Ethernet Interface"
        elif interface_name.startswith('tun') or interface_name.startswith('tap'):
            return "VPN Tunnel Interface"
        elif interface_name.startswith('bond'):
            return "Bonding Interface"
        elif '.' in interface_name:
            return "VLAN Interface"
        elif interface_name == 'lo':
            return "Loopback Interface"
        elif interface_name.startswith('br'):
            return "Bridge Interface"
        else:
            return f"Unknown Adapter ({interface_name})"

    @staticmethod
    def cidr_to_netmask(cidr_bits: int) -> str:
        mask = ('1' * cidr_bits).ljust(32, '0')
        octets = [str(int(mask[i:i + 8], 2)) for i in range(0, 32, 8)]
        return '.'.join(octets)
