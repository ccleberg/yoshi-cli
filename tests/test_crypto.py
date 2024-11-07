"""
Test file for crypto.py
"""

import os
from cryptography.fernet import Fernet
from io import BytesIO
from unittest import TestCase
from crypto import generate_key, load_key, encrypt, decrypt
from unittest.mock import patch

class TestCryptoFunctions(unittest.TestCase):
    """
    This test class checks the functionality of various encryption and
    decryption functions.
    
    The tests cover key generation, loading, and usage in both encryption and
    decryption processes.
    """

    def setUp(self):
        """Initialize test environment by generating a new key."""
        self.key = generate_key()
        with open('vault.sqlite', 'wb') as vault:
            vault.write(b'Hello, world!')

    def tearDown(self):
        """Clean up test data after each test."""
        try:
            os.remove('vault.sqlite')
        except FileNotFoundError:
            pass

    def test_generate_key(self):
        """Test that generate_key() returns a new key on each call."""
        new_key = generate_key()
        self.assertNotEqual(new_key, self.key)

    def test_load_key(self):
        """
        Test that load_key() loads and returns the correct key from file.
        
        This function also checks for a FileNotFoundError when loading an
        invalid key file.
        """
        key_file = 'key.bin'
        with open(key_file, 'wb') as key:
            key.write(self.key)
        loaded_key = load_key(key_file)
        self.assertEqual(loaded_key, self.key)

    def test_encrypt_decrypt(self):
        """Test the end-to-end encryption and decryption process."""
        encrypt(self.key, filename='vault.sqlite')
        with open('vault.sqlite', 'rb') as vault:
            encrypted_data = vault.read()
        decrypt(self.key)
        with open('vault.sqlite', 'rb') as vault:
            decrypted_data = vault.read()
        f = Fernet(self.key)
        self.assertEqual(f.decrypt(encrypted_data), b'Hello, world!')

    def test_load_invalid_key(self):
        """Test that load_key() raises a FileNotFoundError for invalid key files."""
        key_file = 'key.bin'
        try:
            load_key(key_file)
            self.fail('Expected FileNotFoundError')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()
