from abc import abstractmethod
from typing import Optional

class CryptoAlgo:
    @abstractmethod
    def encrypt(self, content: str, key: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, key: str, content: str) -> Optional[str]:
        pass