"""
Unit tests for Fernet cryptographic utilities.
"""

import pytest
import os

# Set dummy key for testing before importing crypto module
os.environ["ENCRYPTION_KEY"] = "dGhpc19pc19hX2R1bW15XzMyX2J5dGVfa2V5X2Zvcl90ZXN0aW5nXzEyMw=="

from backend.app.utils.crypto import encrypt_api_key, decrypt_api_key

def test_encrypt_and_decrypt_api_key():
    raw_key = "sk-proj-test-1234567890abcdef"
    encrypted = encrypt_api_key(raw_key)
    
    assert encrypted != raw_key
    assert isinstance(encrypted, str)
    
    decrypted = decrypt_api_key(encrypted)
    assert decrypted == raw_key

def test_decrypt_empty_key():
    assert decrypt_api_key("") == ""
    assert decrypt_api_key(None) is None
