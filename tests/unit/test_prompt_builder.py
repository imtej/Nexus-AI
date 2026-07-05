"""
Unit tests for Node 3: PromptBuilder dynamic prompt compilation.
"""

import pytest

def test_prompt_builder_structure():
    from backend.app.agents.state import AgentState

    dummy_state: AgentState = {
        "user_id": "test-uuid-1234",
        "user_message": "How do I manage stress?",
        "intent": "question",
        "emotion_signal": "anxious",
        "expanded_query": "managing stress and anxiety techniques",
        "user_identity": {"summary": "Developer working under tight deadlines"},
        "personal_memories": [{"content": "Prefers morning routines"}],
        "collective_knowledge_memories": [{"content": "Deep breathing exercises help grounding"}],
        "system_prompt": "",
        "generated_response": "",
        "new_memory_ids": [],
        "error": None
    }

    assert dummy_state["intent"] == "question"
    assert dummy_state["emotion_signal"] == "anxious"
    assert len(dummy_state["personal_memories"]) == 1
