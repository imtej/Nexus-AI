"""
Unit tests for token bucket rate limiting middleware.
"""

import pytest
import time
from backend.app.api.middleware.rate_limit import RateLimiter

def test_rate_limiter_allows_requests():
    limiter = RateLimiter(requests_per_minute=60)
    client_ip = "127.0.0.1"

    # First request should pass
    is_allowed, retry_after = limiter.is_allowed(client_ip)
    assert is_allowed is True
    assert retry_after == 0

def test_rate_limiter_blocks_excess_requests():
    limiter = RateLimiter(requests_per_minute=2)
    client_ip = "192.168.1.100"

    assert limiter.is_allowed(client_ip)[0] is True
    assert limiter.is_allowed(client_ip)[0] is True

    # 3rd request in same window should be blocked
    is_allowed, retry_after = limiter.is_allowed(client_ip)
    assert is_allowed is False
    assert retry_after > 0
