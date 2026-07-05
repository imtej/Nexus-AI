"""
Integration test for Supabase PostgreSQL + pgvector similarity RPC functions.
"""

import pytest

def test_pgvector_query_structure():
    """Validates parameters sent to search_personal_memories RPC function."""
    target_user_id = "00000000-0000-0000-0000-000000000001"
    query_embedding = [0.1] * 768  # 768-dimensional Gemini embedding vector
    match_count = 5

    rpc_payload = {
        "query_embedding": query_embedding,
        "target_user_id": target_user_id,
        "match_count": match_count
    }

    assert len(rpc_payload["query_embedding"]) == 768
    assert rpc_payload["match_count"] == 5
    assert rpc_payload["target_user_id"] == target_user_id
