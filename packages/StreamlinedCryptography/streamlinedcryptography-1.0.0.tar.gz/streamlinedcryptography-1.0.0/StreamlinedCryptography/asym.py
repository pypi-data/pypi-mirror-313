from cryptography.hazmat.primitives.hashes import SHA256, Hash
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec, utils

from StreamlinedCryptography.util.enforce_types import enforce_types
# from StreamlinedCryptography.util.serialization import serialize_list, deserialize_list
# from StreamlinedCryptography.sym import encrypt_symmetric, decrypt_symmetric, derive_symmetric, SymmetricEncryptResult


class AsymmetricError(Exception):
    """
    A class to represent a cryptographic error in asymmetric operations.
    """
    pass


class AsymmetricPrivateKey:
    """
    A class to represent an asymmetric private key.

    Attributes
    ----------
    private_key : ec.EllipticCurvePrivateKey
        The private key object.

    Methods
    -------
    serialize(password: bytes) -> bytes
        Serialize the private key object.

    from_serialized(data: bytes, password: bytes) -> AsymmetricPrivateKey
        Deserialize a serialized private key object.

    unpack() -> ec.EllipticCurvePrivateKey
        Unpack the private key object.

    generate() -> AsymmetricPrivateKey
        Generate a new private key object

    Notes
    -----
    - Uses PEM encoding for serialization. (Requires password)
    """

    @enforce_types()
    def __init__(self, private_key: ec.EllipticCurvePrivateKey):
        self.private_key = private_key

    def serialize(self, password: bytes) -> bytes:
        """
        Serialize the private key object.

        Usage:
            private_key.serialize(password)

        :param password: bytes
        :return: bytes
        :raises: AsymmetricError: if there is an error in serialization
        """
        try:
            return self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password)
            )
        except Exception as e:
            raise AsymmetricError(f"Error in serialization of private key: {e}")

    @staticmethod
    @enforce_types()
    def from_serialized(data: bytes, password: bytes) -> 'AsymmetricPrivateKey':
        """
        Deserialize a serialized private key object.

        Usage:
            AsymmetricPrivateKey.from_serialized(data, password)

        :param data: bytes
        :param password: bytes
        :return: AsymmetricPrivateKey
        """
        try:
            return AsymmetricPrivateKey(
                serialization.load_pem_private_key(data, password=password, backend=default_backend())
            )
        except Exception as e:
            raise AsymmetricError(f"Error in deserialization of private key: {e}")

    def unpack(self):
        return self.private_key

    @staticmethod
    def generate():
        return AsymmetricPrivateKey(ec.generate_private_key(ec.SECP256R1(), default_backend()))


class AsymmetricPublicKey:
    """
    A class to represent an asymmetric private key.

    Attributes
    ----------
    public_key : ec.EllipticCurvePublicKey
        The public key object.

    Methods
    -------
    serialize() -> bytes
        Serialize the public key object.

    from_serialized(data: bytes) -> AsymmetricPublicKey
        Deserialize a serialized public key object.

    from_private_key(private_key: AsymmetricPrivateKey) -> AsymmetricPublicKey
        Generate a public key object from a private key object.

    unpack() -> ec.EllipticCurvePublicKey
        Unpack the public key object.

    Notes
    -----
    - Uses DER encoding for serialization.
    """

    @enforce_types()
    def __init__(self, public_key: ec.EllipticCurvePublicKey):
        self.public_key = public_key

    def serialize(self):
        """
        Serialize the public key object.

        Usage:
            public_key.serialize()

        :return: bytes
        :raises: AsymmetricError: if there is an error in serialization
        """
        try:
            return self.public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        except Exception as e:
            raise AsymmetricError(f"Error in serialization of public key: {e}")

    @staticmethod
    @enforce_types()
    def from_serialized(data: bytes) -> 'AsymmetricPublicKey':
        """
        Deserialize a serialized public key object.

        Usage:
            AsymmetricPublicKey.from_serialized(data)

        :param data: bytes
        :return: AsymmetricPublicKey
        :raises: AsymmetricError: if there is an error in deserialization
        """
        try:
            return AsymmetricPublicKey(
                serialization.load_der_public_key(data, default_backend())
            )
        except Exception as e:
            raise AsymmetricError(f"Error in deserialization of public key: {e}")

    @staticmethod
    def from_private_key(private_key: AsymmetricPrivateKey) -> 'AsymmetricPublicKey':
        """
        Generate a public key object from a private key object.

        Usage:
            AsymmetricPublicKey.from_private_key(private_key)

        :param private_key: AsymmetricPrivateKey
        :return: AsymmetricPublicKey
        """
        return AsymmetricPublicKey(private_key.unpack().public_key())

    def unpack(self) -> ec.EllipticCurvePublicKey:
        """
        Unpack the public key object.

        Usage:
            public_key.unpack()

        :return: ec.EllipticCurvePublicKey
        """
        return self.public_key


# class AsymmetricEncryptResult:
#     """
#     A class to represent the result of an asymmetric encryption operation.
#
#     Attributes
#     ----------
#     symmetric_result : SymmetricEncryptResult
#         The result of the symmetric encryption operation.
#     ephemeral_public_key : AsymmetricPublicKey
#         The ephemeral public key used in the encryption operation.
#
#     Methods
#     -------
#     serialize() -> bytes
#         Serialize the AsymmetricEncryptResult object.
#
#     from_serialized(serialized_data: bytes) -> AsymmetricEncryptResult
#         Deserialize a serialized AsymmetricEncryptResult object.
#
#     unpack() -> tuple[SymmetricEncryptResult, AsymmetricPublicKey]
#         Unpack the AsymmetricEncryptResult object into a tuple.
#     """
#     def __init__(self, symmetric_encrypt_result: SymmetricEncryptResult, ephemeral_public_key: AsymmetricPublicKey):
#         self.symmetric_result = symmetric_encrypt_result
#         self.ephemeral_public_key = ephemeral_public_key
#
#     def serialize(self) -> bytes:
#         """
#         Serialize the AsymmetricEncryptResult object.
#
#         Usage:
#             result.serialize()
#
#         :return: bytes
#         """
#         return serialize_list((self.symmetric_result.serialize(), self.ephemeral_public_key.serialize()))
#
#     @staticmethod
#     def from_serialized(serialized_data: bytes) -> 'AsymmetricEncryptResult':
#         """
#         Deserialize a serialized AsymmetricEncryptResult object.
#
#         Usage:
#             AsymmetricEncryptResult.from_serialized(serialized_data)
#
#         :param serialized_data:  bytes
#         :return: AsymmetricEncryptResult
#         """
#         salt, nonce, ciphertext, ephemeral_public_key = deserialize_list(serialized_data)
#
#         symmetric_encrypt_result = SymmetricEncryptResult(salt, nonce, ciphertext)
#         ephemeral_public_key = AsymmetricPublicKey.from_serialized(ephemeral_public_key)
#
#         return AsymmetricEncryptResult(symmetric_encrypt_result, ephemeral_public_key)
#
#     def unpack(self) -> tuple[SymmetricEncryptResult, AsymmetricPublicKey]:
#         """
#         Unpack the AsymmetricEncryptResult object into a tuple.
#
#         Usage:
#             result.unpack()
#
#         :return: tuple[SymmetricEncryptResult, AsymmetricPublicKey]
#         """
#         return self.symmetric_result, self.ephemeral_public_key


def derive_secret(private_key: AsymmetricPrivateKey, public_key: AsymmetricPublicKey) -> bytes:
    """
    Derive a shared secret from a private key and a public key.

    Usage:
        derive_secret(private_key, public_key)

    :param private_key: AsymmetricPrivateKey
    :param public_key: AsymmetricPublicKey
    :return: bytes
    """
    try:
        return private_key.unpack().exchange(ec.ECDH(), public_key.unpack())
    except Exception as e:
        raise AsymmetricError(f"Failed to derive shared secret: {e}")


def sign_message(private_key: AsymmetricPrivateKey, message: bytes) -> bytes:
    """
    Sign a message using the private key.
    """
    digest = Hash(SHA256())
    digest.update(message)
    message_hash = digest.finalize()

    return private_key.unpack().sign(
        message_hash,
        ec.ECDSA(
            utils.Prehashed(SHA256())
        )
    )


def verify_signature(public_key: AsymmetricPublicKey, message: bytes, signature: bytes) -> bool:
    """
    Verify a message signature using the public key.
    """

    digest = Hash(SHA256())
    digest.update(message)
    message_hash = digest.finalize()

    try:
        public_key.unpack().verify(
            signature,
            message_hash,
            ec.ECDSA(
                utils.Prehashed(SHA256())
            )
        )
        return True
    except InvalidSignature:
        return False


# def encrypt_asymmetric(private_key: AsymmetricPrivateKey, plaintext: bytes) -> AsymmetricEncryptResult:
#     """
#     Encrypt plaintext using an asymmetric public key.
#
#     Usage:
#         encrypt_asymmetric(public_key, plaintext)
#
#     :param private_key: AsymmetricPrivateKey
#     :param plaintext: bytes
#     :return: bytes
#     """
#
#     salt = urandom(16)
#
#     shared_secret = derive_secret(ephemeral_private_key, ephemeral_public_key)
#
#     shared_key = derive_symmetric(shared_secret, salt)
#
#     try:
#         encrypted = encrypt_symmetric(shared_key, plaintext)
#         return AsymmetricEncryptResult(encrypted, ephemeral_public_key)
#     except Exception as e:
#         raise AsymmetricError(f"Failed to encrypt message: {e}")
#
#
# def decrypt_asymmetric(private_key: AsymmetricPrivateKey, public_key: AsymmetricPublicKey, encrypt_result: AsymmetricEncryptResult) -> bytes:
#     """
#     Decrypt an AsymmetricEncryptResult object using a public key.
#
#     Usage:
#         decrypt_asymmetric(public_key, encrypt_result)
#
#     :param private_key: AsymmetricPrivateKey
#     :param public_key: AsymmetricPublicKey
#     :param encrypt_result: AsymmetricEncryptResult
#     :return: bytes
#     """
#     symmetric_result = encrypt_result.unpack()
#
#     shared_secret = derive_secret(private_key, ephemeral_public_key)
#
#     shared_key = derive_symmetric(shared_secret, symmetric_result.salt)
#
#     try:
#         return decrypt_symmetric(shared_key, symmetric_result)
#     except Exception as e:
#         raise AsymmetricError(f"Failed to decrypt message: {e}")
