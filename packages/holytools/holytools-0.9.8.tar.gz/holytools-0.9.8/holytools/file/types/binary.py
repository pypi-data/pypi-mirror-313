from .file import File
import base64

class BinaryFile(File):
    def read(self) -> bytes:
        return self.as_bytes()

    def write(self,content: bytes):
        with open(self.fpath, 'wb') as file:
            file.write(content)

    def view(self):
        content = self.read()
        hex_content = content.hex()
        for i in range(0, len(hex_content), 20):
            line = ' '.join(hex_content[j:j + 2] for j in range(i, min(i + 20, len(hex_content)), 2))
            print(line)

    def decode(self, encoding='utf-8', error_handling='strict') -> str:
        content = self.read()
        return content.decode(encoding, errors=error_handling)


class BytesConverter:
    @staticmethod
    def to_base64(data : bytes) -> str:
        return base64.b64encode(data).decode(encoding='utf-8')

    @staticmethod
    def from_base64(data : str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def from_hex(data : str) -> bytes:
        return bytes.fromhex(data)

    @staticmethod
    def to_hex(data : bytes) -> str:
        return data.hex()

    @staticmethod
    def decode(data : bytes) -> str:
        return data.decode()

    @staticmethod
    def encode(data : str) -> bytes:
        return data.encode()