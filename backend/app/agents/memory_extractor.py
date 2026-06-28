"""
Nexus AI — Node 5: MemoryExtractor Agent
Extracts and stores memories from conversations (runs async, post-response).
"""

import json
import asyncio
import structlog
from pydantic import BaseModel, Field
from app.agents.state import WorkflowState
from app.services.llm_service import LLMService
from app.services.memory_service import MemoryService
from app.models.memory import MemoryNodeCreate

logger = structlog.get_logger()

class ExtractedMemory(BaseModel):
    content: str = Field(description="What should be remembered (concise, specific)")
    memory_type: str = Field(description="One of: personal_identity, preference, factual, emotional_state")
    tags: list[str] = Field(description="1-3 relevant tags")

class ExtractedMemoryList(BaseModel):
    memories: list[ExtractedMemory] = Field(description="List of extracted memories. Empty if nothing meaningful.", default_factory=list)

EXTRACTION_PROMPT = """Analyze this conversation turn and extract key memories worth remembering about the user.

User message: "{user_message}"
Assistant response: "{assistant_response}"

Extract 0-3 memories. For each memory:
1. "content": What should be remembered (concise, specific)
2. "memory_type": One of: personal_identity, preference, factual, emotional_state
3. "tags": 1-3 relevant tags

Rules:
- Only extract genuinely meaningful information
- Skip generic small talk like "hi" "how are you"
- Focus on what reveals the person's character, preferences, knowledge, or emotional state
- If nothing meaningful, return an empty array

Respond with ONLY valid JSON array: [{{"content": "...", "memory_type": "...", "tags": ["..."]}}]
If nothing to extract, respond with: []"""


async def memory_extractor_node(state: WorkflowState) -> dict:
    """Node 5 — Extract and store memories from the conversation."""
    logger.info("memory_extractor_start", user_id=state.user_id)

    if not state.response:
        return {"new_memory_ids": []}
        
    logger.info("memory_extractor_delay", seconds=5)
    await asyncio.sleep(5)

    try:
        llm = LLMService(
            provider=state.llm_provider,
            api_key=state.llm_api_key or "",
        )

        prompt = EXTRACTION_PROMPT.format(
            user_message=state.user_message,
            assistant_response=state.response,
        )

        # Pydantic Structured Outputs automatically handle LLM JSON constraints
        extraction = await llm.fast_extract(prompt, schema=ExtractedMemoryList)
        memories_data = extraction.memories

        # Store each memory
        memory_service = MemoryService()
        new_ids = []

        for mem in memories_data[:3]:  # Max 3 memories per turn
            try:
                memory_create = MemoryNodeCreate(
                    content=mem.content,
                    memory_type=mem.memory_type,
                    tags=mem.tags,
                )
                stored = await memory_service.store_memory(
                    user_id=state.user_id,
                    memory=memory_create,
                )
                new_ids.append(stored.id)
            except Exception as e:
                logger.warning("memory_extractor_memory_store_fail", error=str(e))
                continue

        logger.info("memory_extractor_complete", memories_stored=len(new_ids))
        return {"new_memory_ids": new_ids}

    except Exception as e:
        logger.warning("memory_extractor_error", error=str(e))
        return {"new_memory_ids": []}
