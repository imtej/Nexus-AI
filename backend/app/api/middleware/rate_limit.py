"""
Nexus AI — Rate Limiting Middleware
Simple in-memory rate limiter for API endpoints.
"""

import time
import structlog
from collections import defaultdict
from fastapi import Request, HTTPException

logger = structlog.get_logger()

# In-memory store: {user_id: [(timestamp, ...)]}
_rate_store: dict[str, list[float]] = defaultdict(list)

# Config
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 20  # max requests per window
CHAT_RATE_LIMIT = 10  # stricter limit for chat endpoint


def _cleanup_old_entries(entries: list[float], window: int) -> list[float]:
    """Remove entries older than the window."""
    cutoff = time.time() - window
    return [t for t in entries if t > cutoff]


async def check_rate_limit(
    request: Request,
    user_id: str,
    max_requests: int = RATE_LIMIT_MAX_REQUESTS,
    window: int = RATE_LIMIT_WINDOW,
) -> None:
    """Check if a user has exceeded the rate limit.
    
    Args:
        request: The FastAPI request object
        user_id: The authenticated user's ID
        max_requests: Maximum requests per window
        window: Time window in seconds
    
    Raises:
        HTTPException 429 if rate limit exceeded
    """
    key = f"{user_id}:{request.url.path}"

    # Cleanup old entries
    _rate_store[key] = _cleanup_old_entries(_rate_store[key], window)

    # Check limit
    if len(_rate_store[key]) >= max_requests:
        retry_after = int(window - (time.time() - _rate_store[key][0]))
        logger.warning(
            "rate_limit_exceeded",
            user_id=user_id,
            path=request.url.path,
            count=len(_rate_store[key]),
        )
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Please try again in {retry_after} seconds.",
            headers={"Retry-After": str(retry_after)},
        )

    # Record this request
    _rate_store[key].append(time.time())


async def check_chat_rate_limit(request: Request, user_id: str) -> None:
    """Stricter rate limit specifically for chat endpoints."""
    await check_rate_limit(
        request, user_id, max_requests=CHAT_RATE_LIMIT, window=RATE_LIMIT_WINDOW
    )
