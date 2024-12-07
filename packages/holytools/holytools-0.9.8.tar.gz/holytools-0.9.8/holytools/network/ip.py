import socket
from enum import Enum
import subprocess
import requests
from holytools.network.adapter import Adapter


class NetworkArea(Enum):
    LOCALHOST  = 'LOCALHOST'
    HOME = 'HOME'
    GLOBAL = 'WAN'


class IpProvider:
    @classmethod
    def get_localhost(cls) -> str:
        return cls.get_ip(area=NetworkArea.LOCALHOST)

    @classmethod
    def get_ip(cls, area: NetworkArea) -> str:
        if area == NetworkArea.LOCALHOST:
            return '127.0.0.1'
        if area == NetworkArea.HOME:
            return cls.get_private_ip()
        if area == NetworkArea.GLOBAL:
            raise PermissionError("Unable to retrieve Global IP automatically. Please check manually")

    @staticmethod
    def get_private_ip() -> str:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            random_ip = '10.254.254.254'
            s.connect((random_ip, 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    @staticmethod
    def get_public_ip() -> str:
        err, public_ip = None, None
        try:
            response = requests.get('https://api.ipify.org')
            if response.status_code == 200:
                public_ip = response.text
            else:
                err = ConnectionError(f'Unable to retrieve public IP: {response.status_code}')
        except Exception as e:
            err = e
        if err:
            raise err
        return public_ip


    @staticmethod
    def get_ipconfig() -> str:
        command = "nmcli device show"
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise Exception(f"Error executing nmcli: {error.decode()}")

        ipconfig = ''
        sections = "".join(output.decode()).split("\n\n")

        for section in sections:
            if section.strip():
                new_adapter = Adapter.from_nmcli_output(section)
                ipconfig += f'\n\n{new_adapter}'

        return ipconfig


if __name__ == "__main__":
    print(IpProvider.get_ipconfig())
