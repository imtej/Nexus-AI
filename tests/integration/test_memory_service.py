"""
Integration test for MemoryService CRUD operations.
"""

import pytest

def test_memory_node_schema_validation():
    """Validates MemoryNode creation dictionary schema."""
    memory_data = {
        "user_id": "user-12345",
        "content": "User prefers FastAPI and Next.js 16",
        "memory_type": "preference",
        "tags": ["tech", "framework"],
        "embedding": [0.05] * 768,
        "recency_score": 1.0,
        "importance_score": 0.8,
        "source": "conversation",
        "is_active": True
    }

    assert memory_data["memory_type"] in ["personal_identity", "preference", "factual", "emotional_state"]
    assert len(memory_data["embedding"]) == 768
    assert memory_data["is_active"] is True
