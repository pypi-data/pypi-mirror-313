from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes
import base64
from .algo import CryptoAlgo


class RSA(CryptoAlgo):

    def encrypt(self, content: str, public_key: bytes) -> str:
        public_key_obj = self._load_public_key(public_key)
        oaep_padding = self._get_padding()
        encrypted = public_key_obj.encrypt(content.encode(), oaep_padding)
        return base64.b64encode(encrypted).decode('utf-8')

    def decrypt(self, private_key: bytes, content: str) -> str:
        private_key_obj = self._load_private_key(private_key)
        oaep_padding = self._get_padding()
        decrypted = private_key_obj.decrypt(base64.b64decode(content), oaep_padding)
        return decrypted.decode('utf-8')

    @staticmethod
    def _get_padding():
        return padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )

    @staticmethod
    def _load_public_key(public_key: bytes):
        return serialization.load_pem_public_key(public_key)

    @staticmethod
    def _load_private_key(private_key: bytes):
        return serialization.load_pem_private_key(private_key, password=None)


    @staticmethod
    def get_key_pair(key_size: int = 2048):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        public_key = private_key.public_key()
        return private_key, public_key


    @staticmethod
    def get_pem(key, is_private: bool):
        kwargs = {
            'encoding': serialization.Encoding.PEM,
            'format': serialization.PrivateFormat.PKCS8 if is_private else serialization.PublicFormat.SubjectPublicKeyInfo,
        }

        if is_private:
            key_bytes = key.private_bytes
            kwargs['encryption_algorithm'] = serialization.NoEncryption()
        else:
            key_bytes = key.public_bytes

        return key_bytes(**kwargs)