from Crypto.Random import get_random_bytes

from strideutils import cryptography


def test_encryption():
    key = get_random_bytes(32)

    # The message to encrypt
    message = "hello"

    # Encrypt the message
    encrypted, iv = cryptography.encrypt_message(message, key)

    # Decrypt the message
    decrypted = cryptography.decrypt_message(encrypted, iv, key)
    assert decrypted == message
