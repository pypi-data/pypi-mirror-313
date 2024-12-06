# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# import os
#
#
# def derive_key(password: str, salt: bytes, key_length: int = 16) -> bytes:
#     kdf = PBKDF2HMAC(
#         algorithm=hashes.SHA256(),
#         length=key_length,
#         salt=salt,
#         iterations=100000,
#         backend=default_backend()
#     )
#     return kdf.derive(password.encode())  # Convert the password to bytes
#
#
# if __name__ == "__main__":
#     test_salt = os.urandom(16)  # Generate a new salt for each password
#     key = derive_key("your_password_here", test_salt)
#     iv = derive_key("your_password_here", test_salt, key_length=16)  # Use a different salt or function for IV
#     print(key, iv)
