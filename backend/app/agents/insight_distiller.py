"""
Nexus AI — Node 6B: Insight Distiller Agent
Distills patterns across users into Collective Knowledge insights (periodic/cron).
"""

import json
import structlog
from pydantic import BaseModel
from app.services.supabase_client import get_supabase_admin
from app.services.llm_service import get_default_llm_service
from app.services.embedding_service import generate_embedding
from app.config.settings import get_settings

logger = structlog.get_logger()

# Structured Output Schema
class CollectiveKnowledgeInsight(BaseModel):
    content: str
    category: str
    tags: list[str]

class CollectiveKnowledgeInsightList(BaseModel):
    insights: list[CollectiveKnowledgeInsight]

DISTILLATION_PROMPT = """You are the Collective Knowledge Distiller. Analyze these anonymized memory patterns from multiple users
and extract universal insights worth adding to the collective wisdom.

Memory patterns (grouped by similarity):
{patterns}

Rules:
1. NEVER include identifying information about any individual
2. Focus on universal human patterns, wisdom, and insights
3. Only extract genuinely valuable insights (not generic platitudes)
4. Quality over quantity — be selective

Return a JSON array of insights:
[{{"content": "...", "category": "wisdom|pattern|knowledge|empathy", "tags": ["..."]}}]

If no meaningful patterns found, return: []"""


async def run_insight_distillation_cycle():
    """Run a full Collective Knowledge distillation cycle. Called periodically."""
    logger.info("insight_distillation_cycle_start")

    db = get_supabase_admin()
    settings = get_settings()

    try:
        # Minimum chunk size needed to recognize universal patterns
        MINIMUM_PATTERN_BATCH = 15

        # 1. Find the timestamp of the last successful curation
        last_collective_knowledge = (
            db.table("collective_knowledge")
            .select("created_at")
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        # 2. Get un-curated memories chronologically
        query = db.table("nexus_memory_nodes").select("content, memory_type, tags").eq("is_active", True)

        if last_collective_knowledge.data:
            last_curated_time = last_collective_knowledge.data[0]["created_at"]
            query = query.filter("created_at", "gt", last_curated_time)

        # Process from oldest to newest to maintain linear timeline
        result = query.order("created_at", desc=False).limit(100).execute()

        new_memories_count = len(result.data) if result.data else 0

        if new_memories_count < MINIMUM_PATTERN_BATCH:
            logger.info("insight_distillation_insufficient_new_data", new_memories=new_memories_count, required=MINIMUM_PATTERN_BATCH)
            return

        # Group patterns (anonymized)
        patterns_text = "\n".join(
            f"- [{m['memory_type']}] {m['content']}" for m in result.data
        )

        llm = get_default_llm_service()
        prompt = DISTILLATION_PROMPT.format(patterns=patterns_text)
        
        # Pydantic Structured Output handles all JSON formatting and extraction flawlessly
        response_model = await llm.fast_extract(prompt, schema=CollectiveKnowledgeInsightList)
        insights = response_model.insights

        if not insights:
            return

        # Store insights in collective_knowledge table
        stored_count = 0
        for insight in insights[:10]: # Limit to max 10 insights per run why? because for the time being we have limited memory nodes to process
            try:
                embedding = await generate_embedding(insight.content)

                db.table("collective_knowledge").insert({
                    "content": insight.content,
                    "category": insight.category,
                    "tags": insight.tags,
                    "embedding": embedding,
                    "contributor_count": len(result.data),
                    "quality_score": 0.7,
                }).execute()

                stored_count += 1
            except Exception as e:
                logger.warning("insight_distillation_insight_store_fail", error=str(e))
                continue

        logger.info("insight_distillation_cycle_complete", insights_stored=stored_count)

    except Exception as e:
        logger.error("insight_distillation_cycle_error", error=str(e))
