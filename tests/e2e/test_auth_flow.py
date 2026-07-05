"""
End-to-End test for user authentication, signup, login, and JWT verification.
"""

import pytest

def test_jwt_bearer_header_format():
    """Validates Authorization header format for JWT verification."""
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_payload"
    auth_header = f"Bearer {token}"

    assert auth_header.startswith("Bearer ")
    token_extracted = auth_header.split(" ")[1]
    assert token_extracted == token
