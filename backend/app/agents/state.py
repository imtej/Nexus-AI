"""
Nexus AI — LangGraph State Schema
Shared state that flows through the agent workflow.
"""

from typing import Optional, Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages

from app.models.memory import MemoryNode, MemorySearchResult, CollectiveKnowledgeInsight
from app.models.user import UserIdentity


class WorkflowState(BaseModel):
    """State schema for the LangGraph workflow."""

    # --- Input ---
    user_id: str
    user_name: Optional[str] = None
    user_message: str
    conversation_id: Optional[str] = None
    conversation_history: list[dict] = Field(default_factory=list)

    # --- QueryAnalyzer output ---
    intent: Optional[str] = None
    emotion_signal: Optional[str] = None
    search_query: Optional[str] = None

    # --- ContextRetriever output ---
    user_identity: Optional[UserIdentity] = None
    personal_memories: list[MemorySearchResult] = Field(default_factory=list)
    collective_knowledge: list[CollectiveKnowledgeInsight] = Field(default_factory=list)

    # --- PromptBuilder output ---
    system_prompt: Optional[str] = None

    # --- ResponseGenerator output ---
    response: Optional[str] = None
    response_chunks: list[str] = Field(default_factory=list)

    # --- MemoryExtractor output ---
    new_memory_ids: list[str] = Field(default_factory=list)

    # --- Metadata ---
    llm_provider: str = "gemini"
    llm_api_key: Optional[str] = None
    is_trial_chat: bool = False
    error: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
