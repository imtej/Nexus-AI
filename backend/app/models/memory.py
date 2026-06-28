"""
Nexus AI — Memory Data Models
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid
import json


class MemoryType(str, Enum):
    PERSONAL_IDENTITY = "personal_identity"
    PREFERENCE = "preference"
    FACTUAL = "factual"
    EMOTIONAL_STATE = "emotional_state"


class CollectiveKnowledgeCategory(str, Enum):
    WISDOM = "wisdom"
    PATTERN = "pattern"
    KNOWLEDGE = "knowledge"
    EMPATHY = "empathy"


class MemoryNode(BaseModel):
    """A single memory unit stored per user."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    content: str
    memory_type: MemoryType
    tags: list[str] = Field(default_factory=list)
    embedding: Optional[list[float]] = None
    recency_score: float = 1.0
    importance_score: float = 0.5
    access_count: int = 0
    source: str = "conversation"
    is_active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("embedding", mode="before")
    @classmethod
    def parse_embedding(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                pass
        return v

    class Config:
        use_enum_values = True


class MemoryNodeCreate(BaseModel):
    """Schema for creating a new memory node."""
    content: str
    memory_type: MemoryType
    tags: list[str] = Field(default_factory=list)

    class Config:
        use_enum_values = True


class CollectiveKnowledgeInsight(BaseModel):
    """A shared, anonymized insight in the Collective Knowledge Base."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    category: CollectiveKnowledgeCategory
    tags: list[str] = Field(default_factory=list)
    embedding: Optional[list[float]] = None
    contributor_count: int = 1
    quality_score: float = 0.5
    is_verified: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_validator("embedding", mode="before")
    @classmethod
    def parse_embedding(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except Exception:
                pass
        return v

    class Config:
        use_enum_values = True


class MemorySearchResult(BaseModel):
    """Result from a memory search."""
    memory: MemoryNode
    similarity_score: float = 0.0
