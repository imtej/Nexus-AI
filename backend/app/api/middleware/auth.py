"""
Nexus AI — Auth Middleware
Verifies Supabase JWT tokens from the Authorization header.
"""

import structlog
from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.config.settings import get_settings

logger = structlog.get_logger()


async def get_current_user(request: Request) -> dict:
    """Extract and verify Supabase JWT from Authorization header.
    
    Returns:
        dict with 'sub' (user_id), 'email', and other JWT claims.
    """
    from app.services.supabase_client import get_supabase_client
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header",
        )

    token = auth_header.split(" ")[1]
    client = get_supabase_client()

    try:
        response = client.auth.get_user(token)
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid token: no user returned")
            
        return {
            "user_id": response.user.id,
            "email": response.user.email,
            "role": response.user.role or "authenticated",
        }
    except Exception as e:
        logger.warning("jwt_verification_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired token")
