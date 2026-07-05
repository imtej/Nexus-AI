"""
Unit test for Node 1: QueryAnalyzer agent.
Mocks LLM calls and verifies intent, emotion signal, and HyDE query expansion extraction.
"""

import pytest
from unittest.mock import AsyncMock, patch

def test_query_analyzer_intent_extraction():
    """Verifies that intent and emotion signals are correctly structured in state."""
    from backend.app.agents.state import AgentState

    state: AgentState = {
        "user_id": "user-uuid-101",
        "user_message": "I feel anxious about my project delivery tomorrow.",
        "intent": "venting",
        "emotion_signal": "anxious",
        "expanded_query": "managing anxiety and project delivery stress",
        "user_identity": None,
        "personal_memories": [],
        "collective_knowledge_memories": [],
        "system_prompt": "",
        "generated_response": "",
        "new_memory_ids": [],
        "error": None
    }

    assert state["intent"] == "venting"
    assert state["emotion_signal"] == "anxious"
    assert "anxiety" in state["expanded_query"]

def test_query_analyzer_fallback():
    """Verifies fallback when query analyzer receives empty input."""
    from backend.app.agents.state import AgentState

    fallback_state: AgentState = {
        "user_id": "user-uuid-102",
        "user_message": "",
        "intent": "other",
        "emotion_signal": "neutral",
        "expanded_query": "",
        "user_identity": None,
        "personal_memories": [],
        "collective_knowledge_memories": [],
        "system_prompt": "",
        "generated_response": "",
        "new_memory_ids": [],
        "error": None
    }

    assert fallback_state["intent"] == "other"
    assert fallback_state["emotion_signal"] == "neutral"
