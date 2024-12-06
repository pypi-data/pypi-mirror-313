import logging

from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Protocol.KDF import PBKDF2

from decentnet.consensus.dev_constants import RUN_IN_DEBUG
from decentnet.modules.logger.log import setup_logger

logger = logging.getLogger(__name__)

setup_logger(RUN_IN_DEBUG, logger)


def derive_key(salt: bytes, password: bytes, iterations: int, key_length: int) -> bytes:
    """
    Derives a key from the provided salt and password using PBKDF2.

    Args:
        salt: The salt value used in key derivation.
        password: The password to derive the key from.
        iterations: The number of iterations for the key derivation algorithm.
        key_length: The desired length of the derived key in bytes.

    Returns:
        The derived key.

    """
    key = PBKDF2(password, salt, dkLen=key_length, count=iterations)
    return key


def encrypt_data(key: bytes, nonce: bytes, plaintext: bytes, aad: bytes) -> bytes:
    """
    Encrypts the provided plaintext using ChaCha20-Poly1305.

    Args:
        key: The encryption key.
        nonce: The nonce value for the encryption.
        plaintext: The data to be encrypted.
        aad: Additional authenticated data.

    Returns:
        The ciphertext.

    """
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return ciphertext + tag


def decrypt_data(key: bytes, nonce: bytes, ciphertext: bytes, aad: bytes) -> bytes:
    """
    Decrypts the provided ciphertext using ChaCha20-Poly1305.

    Args:
        key: The decryption key.
        nonce: The nonce value for the decryption.
        ciphertext: The data to be decrypted.
        aad: Additional authenticated data.

    Returns:
        The decrypted plaintext.

    """
    cipher = ChaCha20_Poly1305.new(key=key, nonce=nonce)
    cipher.update(aad)
    # Separate the tag from the ciphertext (last 16 bytes are the tag)
    tag = ciphertext[-16:]
    ciphertext = ciphertext[:-16]
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext
