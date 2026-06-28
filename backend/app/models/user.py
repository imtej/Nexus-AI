"""
Nexus AI — User Data Models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfile(BaseModel):
    """User profile extending Supabase Auth."""
    id: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    llm_provider: str = "gemini"
    has_api_key: bool = False  # Don't expose actual key
    collective_knowledge_opt_in: bool = True
    free_chats_remaining: int = 4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    llm_provider: Optional[str] = None
    collective_knowledge_opt_in: Optional[bool] = None


class UserIdentity(BaseModel):
    """Nexus AI's understanding of a user."""
    id: Optional[str] = None
    user_id: str
    identity_summary: Optional[str] = None
    traits: dict = Field(default_factory=dict)
    emotional_baseline: Optional[str] = None
    communication_style: Optional[str] = None
    version: int = 1
    updated_at: Optional[datetime] = None


class UserAPIKeyUpdate(BaseModel):
    """Schema for setting user's LLM API key."""
    provider: str  # "gemini", "openai", "anthropic"
    api_key: str
