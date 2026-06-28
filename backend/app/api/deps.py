"""
Nexus AI — API Dependencies
FastAPI dependency injection functions.
"""

from fastapi import Depends, Request
from app.api.middleware.auth import get_current_user
from app.services.supabase_client import get_supabase_admin
from app.services.llm_service import LLMService, get_default_llm_service
from app.utils.crypto import decrypt_api_key


async def get_authenticated_user(request: Request) -> dict:
    """Dependency: Get authenticated user from JWT."""
    return await get_current_user(request)


async def get_llm_for_user(request: Request) -> LLMService:
    """Dependency: Get the appropriate LLM service for the user.
    
    Logic:
    - If user has free chats remaining → use developer's default key
    - If user has their own API key → use their key
    - Otherwise → raise an error asking for API key
    """
    user = await get_current_user(request)
    user_id = user["user_id"]
    db = get_supabase_admin()

    from app.config.settings import get_settings
    settings = get_settings()

    # Get user profile
    profile_result = (
        db.table("nexus_profiles")
        .select("llm_provider, encrypted_api_key, free_chats_used")
        .eq("id", user_id)
        .single()
        .execute()
    )

    profile = profile_result.data
    if not profile:
        # First-time user — create profile with default free chats
        db.table("nexus_profiles").insert({
            "id": user_id,
        }).execute()
        return get_default_llm_service()

    free_chats_used = profile.get("free_chats_used", 0)
    encrypted_key = profile.get("encrypted_api_key")
    provider = profile.get("llm_provider", "gemini")

    if encrypted_key:
        # User has their own key
        api_key = decrypt_api_key(encrypted_key)
        return LLMService(provider=provider, api_key=api_key)
    elif free_chats_used < settings.free_chat_limit:
        # Use developer's default key
        return get_default_llm_service()
    else:
        # No key and no free chats
        from fastapi import HTTPException
        raise HTTPException(
            status_code=402,
            detail="Free trial expired. Please add your API key in settings to continue chatting with Nexus AI.",
        )
