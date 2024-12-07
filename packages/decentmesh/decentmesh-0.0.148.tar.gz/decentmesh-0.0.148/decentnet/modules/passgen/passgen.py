import secrets
import string


class SecurePasswordGenerator:
    def __init__(self, length=16, digits=True, upper=True, lower=True, special=True):
        self.length = length
        self.digits = digits
        self.upper = upper
        self.lower = lower
        self.special = special

    def generate(self):
        characters = ''
        if self.digits:
            characters += string.digits
        if self.upper:
            characters += string.ascii_uppercase
        if self.lower:
            characters += string.ascii_lowercase
        if self.special:
            characters += string.punctuation

        if not characters:
            raise ValueError("At least one character type must be selected")

        # Ensure the generated password is cryptographically secure
        password = ''.join(secrets.choice(characters) for _ in range(self.length))
        return password
