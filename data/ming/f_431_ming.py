import base64
import hashlib
import os

def f_431(password: str, salt_length: int = 8) -> str:
    '''
    Encrypt a password using Salt and SHA-256, then encode the result in base64.

    Parameters:
    password (str): The password to be encrypted.
    salt_length (int, optional): The length of the generated salt. Default is 8.

    Returns:
    str: The encrypted password in base64 format.

    Requirements:
    - base64
    - hashlib
    - os

    Example:
    >>> f_431('my_password')
    '...'  # The actual output will be a base64 encoded string.
    '''
    # Generate a random salt
    salt = os.urandom(salt_length)
    # Use the salt and the password to create a SHA-256 hash
    hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Combine the salt and the hash
    salted_hash = salt + hash
    # Encode the salted hash in base64
    encrypted_password = base64.b64encode(salted_hash)

    return encrypted_password.decode('utf-8')
    

import unittest
import base64
import binascii

def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PasswordEncryptionTests))
    runner = unittest.TextTestRunner()
    runner.run(suite)

class PasswordEncryptionTests(unittest.TestCase):
    
    def test_valid_encryption_format(self):
        encrypted = f_431("test_password")
        try:
            base64.b64decode(encrypted)
            valid = True
        except binascii.Error:
            valid = False
        self.assertTrue(valid)

    def test_varying_password_lengths(self):
        for length in [1, 5, 10, 50, 100]:
            password = "a" * length
            encrypted = f_431(password)
            self.assertTrue(isinstance(encrypted, str) and len(encrypted) > 0)
    
    def test_salt_length_effect(self):
        for salt_length in [1, 4, 8, 16]:
            encrypted = f_431("test_password", salt_length=salt_length)
            self.assertTrue(isinstance(encrypted, str) and len(encrypted) > 0)
    
    def test_special_characters_in_password(self):
        encrypted = f_431("!@#$%^&*()")
        self.assertTrue(isinstance(encrypted, str) and len(encrypted) > 0)
    
    def test_empty_password(self):
        encrypted = f_431("")
        self.assertTrue(isinstance(encrypted, str) and len(encrypted) > 0)
if __name__ == "__main__":
    run_tests()