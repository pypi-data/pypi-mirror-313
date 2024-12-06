from typing import Optional

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from argon2.low_level import hash_secret, Type


class AESCipher:
    def __init__(self, password: bytes, key_size: int = 256, salt: Optional[bytes] = None):
        """
        Initializes the AESCipher with the provided password and key size.
        """
        if key_size not in (128, 192, 256):
            raise ValueError("Key size must be 128, 192, or 256 bits.")
        self.password = password
        self.key_size = key_size
        self.salt = salt if salt is not None else get_random_bytes(16)

    @staticmethod
    def derive_key(password: bytes, salt: bytes, key_length: int) -> bytes:
        """
        Derives a cryptographic key using Argon2 with fast configuration.
        Args:
            password: The password to derive the key from.
            salt: The salt value used in key derivation.
            key_length: The desired length of the derived key in bytes.
        Returns:
            The derived key.
        """
        # Ensure the derived key length matches AES key size (16, 24, or 32 bytes)
        return hash_secret(
            password,
            salt,
            time_cost=1,  # Lower time cost for speed
            memory_cost=8,  # Lower memory cost for speed (8192 KiB)
            parallelism=1,  # Single-threaded for simplicity
            hash_len=key_length // 8,  # key_length is in bits, hash_len expects bytes
            type=Type.ID  # Argon2id (hybrid of Argon2d and Argon2i)
        )

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts the provided plaintext using AES in GCM mode.
        """
        # Derive key according to specified key size (128, 192, or 256 bits)
        key = AESCipher.derive_key(self.password, self.salt, self.key_size)
        nonce = get_random_bytes(12)  # GCM mode uses a 12-byte nonce
        cipher = AES.new(key[:self.key_size // 8], AES.MODE_GCM, nonce=nonce)  # Ensure correct key size
        cipher_text, tag = cipher.encrypt_and_digest(plaintext)
        return self.salt + nonce + tag + cipher_text

    def decrypt(self, cipher_text: bytes) -> bytes:
        """
        Decrypts the provided ciphertext using AES in GCM mode.
        """
        salt = cipher_text[:16]
        nonce = cipher_text[16:28]
        tag = cipher_text[28:44]
        ciphertext_only = cipher_text[44:]
        key = AESCipher.derive_key(self.password, salt, self.key_size)
        cipher = AES.new(key[:self.key_size // 8], AES.MODE_GCM, nonce=nonce)  # Ensure correct key size
        return cipher.decrypt_and_verify(ciphertext_only, tag)
