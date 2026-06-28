"""
Nexus AI — Auth Routes
Auth verification and user info endpoints.
"""

import structlog
from fastapi import APIRouter, Request

from app.api.middleware.auth import get_current_user
from app.services.supabase_client import get_supabase_admin

logger = structlog.get_logger()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me")
async def get_current_user_info(request: Request):
    """Get the current authenticated user's basic info."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    # Get profile
    profile_result = (
        db.table("nexus_profiles")
        .select("id, display_name, avatar_url, free_chats_used")
        .eq("id", user["user_id"])
        .single()
        .execute()
    )

    profile = profile_result.data or {}
    if profile:
        from app.config.settings import get_settings
        settings = get_settings()
        used = profile.get("free_chats_used", 0)
        profile["free_chats_remaining"] = max(0, settings.free_chat_limit - used)

    return {
        "user": {
            "id": user["user_id"],
            "email": user["email"],
            "role": user["role"],
        },
        "profile": profile,
    }


@router.post("/verify")
async def verify_token(request: Request):
    """Verify that a JWT token is valid. Used by frontend for session check."""
    user = await get_current_user(request)
    return {"valid": True, "user_id": user["user_id"]}
