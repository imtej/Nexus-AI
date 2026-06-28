"""
Nexus AI — Conversation Data Models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Message(BaseModel):
    """A single message in a conversation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    conversation_id: str
    role: str  # "user", "assistant", "system"
    content: str
    metadata: dict = Field(default_factory=dict)
    created_at: Optional[datetime] = None


class MessageCreate(BaseModel):
    """Schema for creating a new message."""
    content: str


class Conversation(BaseModel):
    """A conversation between user and Nexus AI."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ConversationWithMessages(Conversation):
    """Conversation with its messages."""
    messages: list[Message] = Field(default_factory=list)


class ChatRequest(BaseModel):
    """Incoming chat request from the frontend."""
    message: str
    conversation_id: Optional[str] = None  # None = new conversation


class ChatResponse(BaseModel):
    """Chat response metadata (actual content is streamed via SSE)."""
    conversation_id: str
    message_id: str
