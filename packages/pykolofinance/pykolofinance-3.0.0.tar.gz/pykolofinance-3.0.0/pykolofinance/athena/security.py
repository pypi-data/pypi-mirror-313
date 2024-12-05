import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from django.conf import settings


class AthenaAESCrypter:
    KEY = settings.ATHENA_CLIENT_KEY
    IV = settings.ATHENA_CLIENT_SECRET

    def encrypt(self, plain_text):
        """
        Encrypts plain text using AES/CBC/PKCS5Padding.

        Args:
            plain_text (str): Text to encrypt.
            key (str): Encryption key (must be 16, 24, or 32 characters).
            iv (str): Initialization vector (must be 16 characters).

        Returns:
            str: Encrypted text (Base64-encoded).
        """

        # Convert key and IV to bytes
        key_bytes = self.KEY.encode('utf-8')[:16]
        iv_bytes = self.IV.encode('utf-8')[:16]
        plain_text_bytes = plain_text.encode('utf-8')

        # Create cipher object
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
        encryptor = cipher.encryptor()

        # Apply PKCS7 padding
        paddler = padding.PKCS7(128).padder()
        padded_data = paddler.update(plain_text_bytes) + paddler.finalize()

        # Encrypt the data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Return Base64-encoded encrypted text
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_text):
        """
        Decrypts encrypted text using AES/CBC/PKCS5Padding.

        Args:
            encrypted_text (str): Base64-encoded encrypted text.
            key (str): Encryption key (must be 16, 24, or 32 characters).
            iv (str): Initialization vector (must be 16 characters).

        Returns:
            str: Decrypted plain text.
        """

        # Convert key and IV to bytes
        key_bytes = self.KEY.encode('utf-8')[:16]
        iv_bytes = self.IV.encode('utf-8')[:16]
        encrypted_bytes = base64.b64decode(encrypted_text)

        # Create cipher object
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv_bytes), backend=default_backend())
        decrypter = cipher.decryptor()

        # Decrypt and remove padding
        decrypted_padded_data = decrypter.update(encrypted_bytes) + decrypter.finalize()
        unpaddler = padding.PKCS7(128).unpadder()
        plain_text_bytes = unpaddler.update(decrypted_padded_data) + unpaddler.finalize()

        # Return the decrypted plain text
        return plain_text_bytes.decode('utf-8')
