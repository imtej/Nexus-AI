"""
RAG Precision & Memory Retrieval Evaluator
Measures precision and recall of retrieved memory nodes for a given query.
"""

def calculate_rag_metrics(retrieved_memories: list, target_memory_types: list) -> dict:
    """
    Calculates precision of memory node retrieval based on expected memory types.
    """
    if not retrieved_memories:
        return {"precision": 0.0, "retrieved_count": 0}

    matching_count = sum(
        1 for mem in retrieved_memories 
        if mem.get("memory_type") in target_memory_types
    )
    
    precision = matching_count / len(retrieved_memories)
    return {
        "precision": round(precision, 2),
        "retrieved_count": len(retrieved_memories),
        "matching_count": matching_count
    }

if __name__ == "__main__":
    sample_retrieved = [
        {"content": "Morning anxiety", "memory_type": "emotional_state"},
        {"content": "Prefers dark mode", "memory_type": "preference"}
    ]
    result = calculate_rag_metrics(sample_retrieved, ["emotional_state"])
    print("RAG Metric Result:", result)
