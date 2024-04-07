import hashlib
import base64

def f_505(filename, data, password):
    """
    Encrypt a string with a password, then write the encrypted string to a file. 
    If the file does not exist, create it.

    Parameters:
    filename (str): The name of the file to write to.
    data (str): The string to encrypt and write to the file.
    password (str): The password to use for encryption.

    Returns:
    str: The encrypted string.

    Requirements:
    - hashlib
    - base64

    Example:
    >>> f_505('test.txt', 'Hello, World!', 'password')
    'Fu0k9LUEJCY+ookLrA=='
    """
    # Ensure the file exists
    try:
        open(filename, 'x').close()
    except FileExistsError:
        pass

    # Encrypt the data using simple XOR operation with password hash as key
    key = hashlib.sha256(password.encode()).digest()
    encrypted_bytes = [byte ^ key[i % len(key)] for i, byte in enumerate(data.encode())]
    encrypted = base64.b64encode(bytes(encrypted_bytes)).decode()

    # Write to the file
    with open(filename, 'w') as f:
        f.write(encrypted)

    return encrypted

import unittest
import hashlib
import base64
import os

def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCases))
    runner = unittest.TextTestRunner()
    runner.run(suite)

class TestCases(unittest.TestCase):
    
    def test_case_1(self):
        # Testing basic encryption and file write
        encrypted = f_505('test1.txt', 'Hello, World!', 'password123')
        with open('test1.txt', 'r') as f:
            file_content = f.read()
        self.assertEqual(encrypted, file_content)
        
    def test_case_2(self):
        # Testing with different data and password
        encrypted = f_505('test2.txt', 'OpenAI', 'secret')
        with open('test2.txt', 'r') as f:
            file_content = f.read()
        self.assertEqual(encrypted, file_content)
        
    def test_case_3(self):
        # Testing with special characters in data and password
        data = '!@#$%^&*()_+'
        password = 'special_chars'
        encrypted = f_505('test3.txt', data, password)
        with open('test3.txt', 'r') as f:
            file_content = f.read()
        self.assertEqual(encrypted, file_content)
        
    def test_case_4(self):
        # Testing file creation if it doesn't exist
        filename = 'nonexistent_file.txt'
        if os.path.exists(filename):
            os.remove(filename)
        encrypted = f_505(filename, 'Test Data', 'pwd')
        self.assertTrue(os.path.exists(filename))
        
    def test_case_5(self):
        # Testing decryption to ensure encryption is reversible
        data = 'Decryption Test'
        password = 'decrypt_pwd'
        encrypted = f_505('test5.txt', data, password)
        
        # Decryption logic (reverse of encryption)
        key = hashlib.sha256(password.encode()).digest()
        decrypted_bytes = [byte ^ key[i % len(key)] for i, byte in enumerate(base64.b64decode(encrypted))]
        decrypted = bytes(decrypted_bytes).decode()
        
        self.assertEqual(data, decrypted)

if __name__ == "__main__":
    run_tests()