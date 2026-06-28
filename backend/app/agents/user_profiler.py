"""
Nexus AI — Node 6A: User Profiler Agent
Forges and incrementally evolves the UserIdentity profile (periodic/cron).
"""

import asyncio
import structlog
from pydantic import BaseModel, Field
from datetime import datetime

from app.services.supabase_client import get_supabase_admin
from app.services.llm_service import get_default_llm_service
from app.services.memory_service import MemoryService
from app.models.user import UserIdentity

logger = structlog.get_logger()

# Pydantic Structured Output Schema
class UserIdentityExtraction(BaseModel):
    identity_summary: str = Field(description="A 2-3 sentence profound summary of who this person is at their core.")
    traits: dict[str, str] = Field(description="A creative dictionary of key traits and their intensities. Keys are lowercase, values are brief descriptions.")
    emotional_baseline: str = Field(description="The user's default emotional baseline (e.g. 'thoughtful but prone to anxiety', 'optimistic and curious').")
    communication_style: str = Field(description="How the user typically communicates (e.g. 'terse and direct', 'elaborate and philosophical').")

PROFILE_EVOLUTION_PROMPT = """You are the Nexus AI Profiler.
Your task is to analyze a user's new memory nodes and incrementally evolve their core psychological identity profile.

{existing_identity_context}

Here are the {memory_count} NEW memories extracted from their recent conversations:
{new_memories_list}

Analyze these new memories. If there is an existing identity, EVOLVE it seamlessly based on this new data. If this is a new identity, build it from scratch.

Extract and return the highly refined UserIdentity structure."""

async def run_user_profiling_cycle():
    """Run a full User Profiler cycle. Called periodically."""
    logger.info("user_profiler_cycle_start")
    
    MINIMUM_NEW_MEMORIES = 5
    # MINIMUM_NEW_MEMORIES = 10

    
    db = get_supabase_admin()
    memory_service = MemoryService()
    
    try:
        # 1. Fetch active users (limit to 50 for safety in a single cycle)
        users_result = db.table("nexus_profiles").select("id, encrypted_api_key, llm_provider").limit(50).execute() # encrypted_api_key and llm_provider are used to determine if the user has provided their own API key
        
        if not users_result.data:
            return
            
        identities_forged = 0

        total_users_considered = len(users_result.data)
        users_insufficient_new_memories = 0

        for user in users_result.data:
            user_id = user["id"]
            
            # Fetch local API key for this user
            from app.utils.crypto import decrypt_api_key
            from app.config.settings import get_settings
            from app.services.llm_service import LLMService

            encrypted_key = user.get("encrypted_api_key")
            if encrypted_key: # User has provided their own API key use that for identity building
                user_api_key = decrypt_api_key(encrypted_key)
                llm = LLMService(
                    provider=user.get("llm_provider", "gemini"),
                    api_key=user_api_key
                )
            else: # If user has not provided their own API key use the default LLM service
                settings = get_settings()
                llm = get_default_llm_service()
                
            # Fetch existing identity
            existing_identity_data = await memory_service.get_user_identity(user_id)
            last_updated = None
            
            existing_context = "This is a brand new user. You are forging their identity for the very first time."
            
            if existing_identity_data:
                last_updated = existing_identity_data.get("updated_at")
                
                # Format existing identity for the prompt
                traits_str = ", ".join([f"{k}: {v}" for k, v in existing_identity_data.get("traits", {}).items()])
                existing_context = (
                    f"EXISTING PSYCHOLOGICAL PROFILE:\n"
                    f"- Summary: {existing_identity_data.get('identity_summary')}\n"
                    f"- Traits: {traits_str}\n"
                    f"- Emotional Baseline: {existing_identity_data.get('emotional_baseline')}\n"
                    f"- Communication Style: {existing_identity_data.get('communication_style')}\n\n"
                    f"Do not overwrite core traits unless the new memories contradict them. Deepen and refine the existing profile."
                )

            # Fetch new memories since last update
            query = db.table("nexus_memory_nodes").select("content, memory_type").eq("user_id", user_id).eq("is_active", True)
            if last_updated:
                query = query.filter("created_at", "gt", last_updated)
                
            memories_result = query.order("created_at", desc=False).execute()
            new_memories = memories_result.data or []
            
            if len(new_memories) < MINIMUM_NEW_MEMORIES:
                users_insufficient_new_memories += 1
                # logger.info("identity_builder_insufficient_new_data", user_id=user_id, new_memories=len(new_memories), required=MINIMUM_NEW_MEMORIES)
                continue
                
                logger.info("user_profiler_processing_user", user_id=user_id, new_memories=len(new_memories))
            
            # Format new memories
            new_memories_list = "\n".join(
                f"- [{m['memory_type']}] {m['content']}" for m in new_memories
            )
            
            prompt = PROFILE_EVOLUTION_PROMPT.format(
                existing_identity_context=existing_context,
                memory_count=len(new_memories),
                new_memories_list=new_memories_list
            )
            
            try:
                # Use native Pydantic extraction
                extraction = await llm.fast_extract(prompt, schema=UserIdentityExtraction)
                
                # Increment version
                new_version = 1
                if existing_identity_data:
                    new_version = existing_identity_data.get("version", 0) + 1
                
                # Upsert to database
                await memory_service.update_user_identity(user_id, {
                    "identity_summary": extraction.identity_summary,
                    "traits": extraction.traits,
                    "emotional_baseline": extraction.emotional_baseline,
                    "communication_style": extraction.communication_style,
                    "version": new_version
                })
                
                identities_forged += 1
                
            except Exception as e:
                logger.error("user_profiler_upsert_error", user_id=user_id, error=str(e))
                continue
        logger.info("user_profiler_insufficient_new_data", users_insufficient_new_memories=users_insufficient_new_memories, total_users_considered=total_users_considered)
        logger.info("user_profiler_cycle_complete", identities_forged=identities_forged, total_users_considered=total_users_considered)
        
    except Exception as e:
        logger.error("user_profiler_cycle_error", error=str(e))
