"""
Nexus AI — Cryptographic Utilities
Handles encryption/decryption of user API keys.
"""

from cryptography.fernet import Fernet
from app.config.settings import get_settings


def get_cipher() -> Fernet:
    """Get Fernet cipher for encryption/decryption."""
    settings = get_settings()
    return Fernet(settings.encryption_key.encode())


def encrypt_api_key(api_key: str) -> str:
    """Encrypt a user's API key for storage."""
    cipher = get_cipher()
    return cipher.encrypt(api_key.encode()).decode()


def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypt a user's stored API key."""
    cipher = get_cipher()
    return cipher.decrypt(encrypted_key.encode()).decode()
