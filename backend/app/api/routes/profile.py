"""
Nexus AI — Profile API Routes
User profile and API key management.
"""

import structlog
from fastapi import APIRouter, HTTPException, Request

from app.api.middleware.auth import get_current_user
from app.services.supabase_client import get_supabase_admin
from app.models.user import UserProfileUpdate, UserAPIKeyUpdate
from app.utils.crypto import encrypt_api_key
from app.config.settings import get_settings

logger = structlog.get_logger()

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("")
async def get_profile(request: Request):
    """Get the current user's profile."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    result = (
        db.table("nexus_profiles")
        .select("id, display_name, avatar_url, llm_provider, collective_knowledge_opt_in, free_chats_used, custom_key_chats_used, created_at")
        .eq("id", user["user_id"])
        .single()
        .execute()
    )

    if not result.data:
        # Create profile if it doesn't exist
        settings = get_settings()
        new_profile = {
            "id": user["user_id"],
            "display_name": user.get("email", "").split("@")[0],
            "free_chats_used": 0,
            "custom_key_chats_used": 0,
        }
        db.table("nexus_profiles").insert(new_profile).execute()
        result = db.table("nexus_profiles").select("*").eq("id", user["user_id"]).single().execute()

    profile = result.data

    # Backwards compatibility: visually supply 'free_chats_remaining' calculated
    # Hide free chats remainder if user supplied their own API key
    settings = get_settings()
    has_key = bool(
        db.table("nexus_profiles")
        .select("encrypted_api_key")
        .eq("id", user["user_id"])
        .single()
        .execute()
        .data.get("encrypted_api_key")
    )
    
    if has_key:
        profile["free_chats_remaining"] = None # User has provided their own API key so Hide free chats remainder
    else:
        used = profile.get("free_chats_used", 0)
        profile["free_chats_remaining"] = max(0, settings.free_chat_limit - used)
        
    profile["has_api_key"] = has_key

    # Remove sensitive field
    profile.pop("encrypted_api_key", None)

    return {"profile": profile}


@router.patch("")
async def update_profile(update: UserProfileUpdate, request: Request):
    """Update user profile."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    update_data = update.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    db.table("nexus_profiles").update(update_data).eq("id", user["user_id"]).execute()

    return {"status": "updated"}


@router.post("/api-key")
async def set_api_key(key_update: UserAPIKeyUpdate, request: Request):
    """Set or update the user's LLM API key."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    if key_update.provider not in ("gemini", "openai", "anthropic"):
        raise HTTPException(status_code=400, detail="Invalid provider. Must be: gemini, openai, anthropic")

    # Encrypt the API key
    encrypted = encrypt_api_key(key_update.api_key)

    db.table("nexus_profiles").update({
        "llm_provider": key_update.provider,
        "encrypted_api_key": encrypted,
    }).eq("id", user["user_id"]).execute()

    logger.info("api_key_set", user_id=user["user_id"], provider=key_update.provider)

    return {"status": "api_key_saved", "provider": key_update.provider}


@router.delete("/api-key")
async def remove_api_key(request: Request):
    """Remove the user's stored API key."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    db.table("nexus_profiles").update({
        "encrypted_api_key": None,
    }).eq("id", user["user_id"]).execute()

    return {"status": "api_key_removed"}
