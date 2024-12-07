from StreamlinedCryptography.util.enforce_types import enforce_types
from StreamlinedCryptography.util.serialization import serialize_list, deserialize_list

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from os import urandom


class SymmetricError(Exception):
    """
    A class to represent a cryptographic error in symmetric operations.
    """
    pass


class SymmetricEncryptResult:
    """
    A class to represent the result of a symmetric encryption operation.

    Attributes
    ----------
    salt : bytes
        The salt used in the encryption operation.
    nonce : bytes
        The nonce used in the encryption operation.
    ciphertext : bytes
        The encrypted ciphertext.

    Methods
    -------
    from_serialized(serialized_data: bytes) -> SymmetricEncryptResult
        Deserialize a serialized SymmetricEncryptResult object.

    unpack() -> tuple[bytes, bytes, bytes]
        Unpack the SymmetricEncryptResult object into a tuple.

    serialize() -> bytes
        Serialize the SymmetricEncryptResult object.
    """

    @enforce_types()
    def __init__(self, salt: bytes, nonce: bytes, ciphertext: bytes):
        if len(salt) != 16:
            raise SymmetricError("Salt length must be 16 bytes")

        if len(nonce) != 12:
            raise SymmetricError("Nonce length must be 12 bytes")

        self.ciphertext = ciphertext
        self.salt = salt
        self.nonce = nonce

    @staticmethod
    @enforce_types()
    def from_serialized(serialized_data: bytes):
        """
        Deserialize a serialized SymmetricEncryptResult object.

        Usage:
            SymmetricEncryptResult.from_serialized(serialized_data)

        :param serialized_data: bytes
        :return: SymmetricEncryptResult
        """
        return SymmetricEncryptResult(*deserialize_list(serialized_data))

    def unpack(self) -> tuple[bytes, bytes, bytes]:
        """
        Unpack the SymmetricEncryptResult object into a tuple.

        Usage:
            result = SymmetricEncryptResult(salt, nonce, ciphertext)
            result.unpack()

        :return: tuple[bytes, bytes, bytes]
        """
        return self.salt, self.nonce, self.ciphertext

    def serialize(self) -> bytes:
        """
        Serialize the SymmetricEncryptResult object.

        Usage:
            result = SymmetricEncryptResult(salt, nonce, ciphertext)
            result.serialize()

        :return: bytes
        """
        return serialize_list(self.unpack())


@enforce_types()
def derive_symmetric(password: bytes, salt: bytes, iterations: int = 100_000, key_len: int = 32) -> bytes:
    """
    Derive a symmetric key from a password and salt.

    Usage:
        derive_symmetric(password, salt, iterations, key_len)

    Notes:
        - Key length should be 32 bytes.

    :param password: bytes
    :param salt: bytes
    :param iterations: int
    :param key_len: int
    :return: bytes
    """

    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=key_len,
        salt=salt,
        iterations=iterations
    )

    return kdf.derive(password)


@enforce_types()
def encrypt_symmetric(password: bytes, plaintext: bytes, associated_data: bytes = None) -> SymmetricEncryptResult:
    """
    Encrypt plaintext using a symmetric key derived from a password.

    Usage:
        encrypt_symmetric(password, plaintext, associated_data)

    :param password: bytes
    :param plaintext: bytes
    :param associated_data: bytes
    :return: SymmetricEncryptResult
    """

    salt = urandom(16)
    nonce = urandom(12)

    key = derive_symmetric(password, salt)

    cipher = AESGCM(key)
    ciphertext = cipher.encrypt(nonce, plaintext, associated_data)

    return SymmetricEncryptResult(salt, nonce, ciphertext)


@enforce_types()
def decrypt_symmetric(password: bytes, encrypt_result: SymmetricEncryptResult, associated_data: bytes = None):
    """
    Decrypt a SymmetricEncryptResult object using a password.

    Usage:
        decrypt_symmetric(password, encrypt_result, associated_data)

    :param password: bytes
    :param encrypt_result: SymmetricEncryptResult
    :param associated_data: bytes
    :return: bytes
    """
    salt, nonce, ciphertext = encrypt_result.unpack()

    key = derive_symmetric(password, salt)

    cipher = AESGCM(key)
    try:
        return cipher.decrypt(nonce, ciphertext, associated_data)
    except Exception as e:
        raise SymmetricError(f"Decryption error: {e}")


if __name__ == '__main__':
    data = "Test Message"
    message_password = "Password"

    print(f'data: {data}')

    encrypted = encrypt_symmetric(message_password.encode(), data.encode())
    serialized = encrypted.serialize()

    print(f'serialized: {serialized}')

    deserialized = SymmetricEncryptResult.from_serialized(serialized)
    decrypted = decrypt_symmetric(message_password.encode(), deserialized).decode()

    print(f'decrypted: {decrypted}')
