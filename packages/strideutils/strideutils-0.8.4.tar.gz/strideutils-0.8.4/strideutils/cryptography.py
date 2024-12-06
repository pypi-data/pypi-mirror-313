import base64
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_message(message: str, key: bytes) -> Tuple[str, str]:
    """
    Encrypt the message using AES in CBC mode.

    Args:
        message: The plaintext message to encrypt
        key: The encryption key (should be 32 bytes for AES-256)

    Returns:
        A tuple of (encrypted_message, initialization_vector), both base64 encoded strings
    """
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)

    # Initialize the cipher for encryption
    cipher_encrypt = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the message.
    # The message needs to be padded to make sure its length is a multiple of the block size.
    encrypted = cipher_encrypt.encrypt(pad(message.encode(), AES.block_size))

    # Return the encrypted data and the IV as base64 encoded strings.
    return base64.b64encode(encrypted).decode(), base64.b64encode(iv).decode()


def decrypt_message(encrypted: str, iv: str, key: bytes) -> str:
    """
    Decrypt the message using AES in CBC mode.

    Args:
        encrypted: The encrypted message as a base64 encoded string
        iv: The initialization vector as a base64 encoded string
        key: The encryption key (should be 32 bytes for AES-256)

    Returns:
        The decrypted plaintext message
    """
    # Decode the encrypted message and IV from base64 to bytes.
    encrypted_bytes = base64.b64decode(encrypted)
    iv_bytes = base64.b64decode(iv)

    # Initialize the cipher for decryption.
    cipher_decrypt = AES.new(key, AES.MODE_CBC, iv_bytes)

    # Decrypt the message and unpad it.
    decrypted = unpad(cipher_decrypt.decrypt(encrypted_bytes), AES.block_size)

    return decrypted.decode()
