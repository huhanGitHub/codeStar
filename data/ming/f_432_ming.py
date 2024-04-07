import base64
import zlib
import random
import string

def f_432(string_length=100):
    """
    Create a random string of a specified length (default is 100), compress it with zlib, 
    and then encode the compressed string in base64.

    Parameters:
    - string_length (int, optional): The length of the random string to be generated. Default is 100.

    Returns:
    str: The compressed string in base64.

    Requirements:
    - base64
    - zlib
    - random
    - string

    Example:
    >>> compressed_string = f_432(50)
    >>> print(compressed_string)
    """
    # Generate a random string
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=string_length))
    
    # Compress the string
    compressed_string = zlib.compress(random_string.encode('utf-8'))
    
    # Encode the compressed string in base64
    encoded_compressed_string = base64.b64encode(compressed_string)

    return encoded_compressed_string.decode('utf-8')

import unittest
import base64
import zlib

def run_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCases))
    runner = unittest.TextTestRunner()
    runner.run(suite)

class TestCases(unittest.TestCase):

    def test_case_1(self):
        result = f_432()
        self.assertIsInstance(result, str)
        decoded_result = base64.b64decode(result)
        decompressed_result = zlib.decompress(decoded_result).decode('utf-8')
        self.assertEqual(len(decompressed_result), 100)

    def test_case_2(self):
        result = f_432(50)
        self.assertIsInstance(result, str)
        decoded_result = base64.b64decode(result)
        decompressed_result = zlib.decompress(decoded_result).decode('utf-8')
        self.assertEqual(len(decompressed_result), 50)

    def test_case_3(self):
        result = f_432(200)
        self.assertIsInstance(result, str)
        decoded_result = base64.b64decode(result)
        decompressed_result = zlib.decompress(decoded_result).decode('utf-8')
        self.assertEqual(len(decompressed_result), 200)

    def test_case_4(self):
        result = f_432(10)
        self.assertIsInstance(result, str)
        decoded_result = base64.b64decode(result)
        decompressed_result = zlib.decompress(decoded_result).decode('utf-8')
        self.assertEqual(len(decompressed_result), 10)

    def test_case_5(self):
        result = f_432(1000)
        self.assertIsInstance(result, str)
        decoded_result = base64.b64decode(result)
        decompressed_result = zlib.decompress(decoded_result).decode('utf-8')
        self.assertEqual(len(decompressed_result), 1000)

if __name__ == "__main__":
    run_tests()