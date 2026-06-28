"""
Nexus AI — Conversation API Routes
CRUD operations for conversations.
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.middleware.auth import get_current_user
from app.services.supabase_client import get_supabase_admin

logger = structlog.get_logger()

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.get("")
async def list_conversations(request: Request):
    """List all conversations for the authenticated user."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    result = (
        db.table("nexus_conversations")
        .select("id, title, created_at, updated_at")
        .eq("user_id", user["user_id"])
        .order("updated_at", desc=True)
        .limit(50)
        .execute()
    )

    return {"conversations": result.data or []}


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str, request: Request):
    """Get a specific conversation with its messages."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    # Verify ownership
    conv_result = (
        db.table("nexus_conversations")
        .select("*")
        .eq("id", conversation_id)
        .eq("user_id", user["user_id"])
        .single()
        .execute()
    )

    if not conv_result.data:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Get messages
    msg_result = (
        db.table("nexus_messages")
        .select("id, role, content, metadata, created_at")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )

    return {
        "conversation": conv_result.data,
        "messages": msg_result.data or [],
    }


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, request: Request):
    """Delete a conversation and its messages."""
    user = await get_current_user(request)
    db = get_supabase_admin()

    # Verify ownership
    conv_result = (
        db.table("nexus_conversations")
        .select("id")
        .eq("id", conversation_id)
        .eq("user_id", user["user_id"])
        .single()
        .execute()
    )

    if not conv_result.data:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Delete messages first (cascade), then conversation
    db.table("nexus_messages").delete().eq("conversation_id", conversation_id).execute()
    db.table("nexus_conversations").delete().eq("id", conversation_id).execute()

    return {"status": "deleted"}


@router.patch("/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    request: Request,
):
    """Update conversation title."""
    user = await get_current_user(request)
    body = await request.json()
    db = get_supabase_admin()

    # Verify ownership
    conv_result = (
        db.table("nexus_conversations")
        .select("id")
        .eq("id", conversation_id)
        .eq("user_id", user["user_id"])
        .single()
        .execute()
    )

    if not conv_result.data:
        raise HTTPException(status_code=404, detail="Conversation not found")

    update_data = {}
    if "title" in body:
        update_data["title"] = body["title"]

    if update_data:
        db.table("nexus_conversations").update(update_data).eq("id", conversation_id).execute()

    return {"status": "updated"}
