# test_crypto.py
import unittest
from io import BytesIO
from cryptography.fernet import Fernet
from crypto import generate_key, load_key, encrypt, decrypt

class TestCryptoFunctions(unittest.TestCase):

    def setUp(self):
        self.key = generate_key()
        with open('vault.sqlite', 'wb') as vault:
            vault.write(b'Hello, world!')

    def tearDown(self):
        try:
            os.remove('vault.sqlite')
        except FileNotFoundError:
            pass

    def test_generate_key(self):
        new_key = generate_key()
        self.assertNotEqual(new_key, self.key)

    def test_load_key(self):
        key_file = 'key.bin'
        with open(key_file, 'wb') as key:
            key.write(self.key)
        loaded_key = load_key(key_file)
        self.assertEqual(loaded_key, self.key)

    def test_encrypt_decrypt(self):
        encrypt(self.key, filename='vault.sqlite')
        with open('vault.sqlite', 'rb') as vault:
            encrypted_data = vault.read()
        decrypt(self.key)
        with open('vault.sqlite', 'rb') as vault:
            decrypted_data = vault.read()
        f = Fernet(self.key)
        self.assertEqual(f.decrypt(encrypted_data), b'Hello, world!')

    def test_load_invalid_key(self):
        key_file = 'key.bin'
        try:
            load_key(key_file)
            self.fail('Expected FileNotFoundError')
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    unittest.main()
