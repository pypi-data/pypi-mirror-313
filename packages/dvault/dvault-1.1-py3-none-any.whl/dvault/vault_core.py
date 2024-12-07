import base64

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

from . import Constants


class VaultCore:
    def __init__(self, password: str):
        kdf = Scrypt(salt=Constants.SALT, length=32, n=2**16, r=8, p=1)
        self.__fernet = Fernet(base64.urlsafe_b64encode(kdf.derive(password.encode())))
        self.__common_prefix = (
            b"\x80"
            + Constants.MY_BIRTH_DAY_UNIX_SECONDS.to_bytes(length=8, byteorder="big")
            + Constants.MY_BIRTH_DAY_BYTE_ARRAY
        )
        self.__common_prefix_len = len(self.__common_prefix)

    def encrypt_bytes(self, input: bytes) -> bytes:
        result = self.__fernet._encrypt_from_parts(
            input,
            Constants.MY_BIRTH_DAY_UNIX_SECONDS,
            Constants.MY_BIRTH_DAY_BYTE_ARRAY,
        )
        return base64.urlsafe_b64decode(result)[self.__common_prefix_len :]

    def decrypt_bytes(self, input: bytes) -> bytes:
        try:
            result = self.__fernet.decrypt(
                base64.urlsafe_b64encode(self.__common_prefix + input)
            )
            return result
        except InvalidToken:
            raise RuntimeError(Constants.ERR_DECRYPT)

    def encrypt_string(self, input: str) -> bytes:
        return self.encrypt_bytes(input.encode())

    def decrypt_string(self, input: bytes) -> str:
        return self.decrypt_bytes(input).decode()
