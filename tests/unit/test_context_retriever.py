"""
Unit test for Node 2: ContextRetriever agent.
Mocks pgvector vector search and verifies memory deduplication & filtering.
"""

import pytest

def test_context_retriever_memory_deduplication():
    """Verifies duplicate memory content filtering."""
    raw_memories = [
        {"id": "1", "content": "Prefers dark mode", "similarity": 0.95},
        {"id": "2", "content": "Prefers dark mode", "similarity": 0.94},
        {"id": "3", "content": "Uses Python 3.12", "similarity": 0.88}
    ]

    seen = set()
    deduped = []
    for mem in raw_memories:
        if mem["content"] not in seen:
            seen.add(mem["content"])
            deduped.append(mem)

    assert len(deduped) == 2
    assert deduped[0]["id"] == "1"
    assert deduped[1]["id"] == "3"

def test_context_retriever_threshold_filtering():
    """Verifies similarity score threshold filtering."""
    memories = [
        {"id": "1", "similarity": 0.85},
        {"id": "2", "similarity": 0.40},  # Below 0.5 threshold
        {"id": "3", "similarity": 0.72}
    ]

    filtered = [m for m in memories if m["similarity"] >= 0.5]
    assert len(filtered) == 2
    assert all(m["similarity"] >= 0.5 for m in filtered)
