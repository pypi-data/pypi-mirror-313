import string
import unittest

from decentnet.modules.passgen.passgen import SecurePasswordGenerator


class TestPasswordGenerator(unittest.TestCase):
    def test_password_content(self):
        # Test parameters
        length = 40
        has_digits = True
        has_upper = True
        has_lower = True
        has_special = True

        # Instantiate the password generator
        generator = SecurePasswordGenerator(length, has_digits, has_upper, has_lower,
                                            has_special)

        # Generate the password
        password = generator.generate()

        # Assert conditions
        if has_digits:
            self.assertTrue(any(char in string.digits for char in password),
                            "Password lacks digits")
        if has_upper:
            self.assertTrue(any(char in string.ascii_uppercase for char in password),
                            "Password lacks uppercase letters")
        if has_lower:
            self.assertTrue(any(char in string.ascii_lowercase for char in password),
                            "Password lacks lowercase letters")
        if has_special:
            self.assertTrue(any(char in string.punctuation for char in password),
                            "Password lacks special characters")

        # Assert length
        self.assertEqual(len(password), length,
                         "Password length does not match the specified length")
        print(password)


if __name__ == '__main__':
    unittest.main()
