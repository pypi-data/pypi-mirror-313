import unittest

from decentnet.modules.cryptography.symetric import AESCipher


class TestAESCipher(unittest.TestCase):

    def test_encrypt_decrypt_with_different_key_sizes(self):
        for key_size in [128, 192, 256]:
            with self.subTest(key_size=key_size):
                password = "testpassword".encode()
                plaintext = b"This is a test message."
                cipher = AESCipher(password=password, key_size=key_size)

                # Encrypt the plaintext
                encrypted_text = cipher.encrypt(plaintext)

                # Decrypt the encrypted text
                decrypted_text = cipher.decrypt(encrypted_text)

                # Assert that the decrypted text is the same as the original plaintext
                self.assertEqual(decrypted_text, plaintext)

    def test_invalid_key_size(self):
        with self.assertRaises(ValueError):
            AESCipher(b"array", 64)  # An unsupported key size


if __name__ == '__main__':
    unittest.main()
