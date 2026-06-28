"""
Nexus AI — Node 7: EvolutionEngine Agent
Updates System's personality traits based on accumulated interactions (periodic/cron).
"""

import structlog
from datetime import datetime
from app.services.supabase_client import get_supabase_admin

logger = structlog.get_logger()


async def run_personality_evolution_cycle():
    """Run a personality evolution cycle. Called periodically."""
    logger.info("evolution_engine_cycle_start")

    db = get_supabase_admin()

    try:
        # Get current evolution state
        evolution_result = db.table("system_evolution").select("*").eq("id", 1).single().execute()

        if not evolution_result.data:
            # Initialize evolution state
            db.table("system_evolution").insert({
                "id": 1,
                "personality_version": "1.0.0",
                "total_interactions": 0,
                "total_users": 0,
                "empathy_depth": 0.1,
                "knowledge_breadth": 0.1,
                "wisdom_score": 0.1,
                "curiosity_level": 0.9,
            }).execute()
            return

        evolution = evolution_result.data

        # Count actual interactions and users
        interaction_count_result = db.table("nexus_messages").select("id", count="exact").eq("role", "user").execute()
        total_interactions = interaction_count_result.count or 0

        user_count_result = db.table("nexus_profiles").select("id", count="exact").execute()
        total_users = user_count_result.count or 0

        # Count memory types for trait calculation
        emotional_memories = db.table("nexus_memory_nodes").select("id", count="exact").eq("memory_type", "emotional_state").execute()
        factual_memories = db.table("nexus_memory_nodes").select("id", count="exact").eq("memory_type", "factual").execute()
        collective_insights = db.table("collective_knowledge").select("id", count="exact").execute()

        emotional_count = emotional_memories.count or 0
        factual_count = factual_memories.count or 0
        hive_count = collective_insights.count or 0

        # Calculate evolution traits (0.0 to 1.0, logarithmic growth)
        import math

        def log_growth(value: int, scale: float = 100.0) -> float:
            """Logarithmic growth from 0.1 to ~0.95."""
            return min(0.95, 0.1 + 0.85 * (math.log(1 + value) / math.log(1 + scale)))

        empathy_depth = log_growth(emotional_count, 500)
        knowledge_breadth = log_growth(factual_count, 500)
        wisdom_score = log_growth(hive_count, 200)
        curiosity_level = max(0.3, 0.9 - log_growth(total_interactions, 5000) * 0.6)

        # Determine version bump
        old_version = evolution.get("personality_version", "1.0.0")
        major, minor, patch = [int(x) for x in old_version.split(".")]

        stage_thresholds = [0, 100, 1000, 10000]
        old_stage = sum(1 for t in stage_thresholds if evolution.get("total_interactions", 0) >= t)
        new_stage = sum(1 for t in stage_thresholds if total_interactions >= t)

        if new_stage > old_stage:
            major += 1
            minor = 0
            patch = 0
        elif total_interactions - evolution.get("total_interactions", 0) > 100:
            minor += 1
            patch = 0
        elif total_interactions - evolution.get("total_interactions", 0) > 10:
            patch += 1
        else:
            pass

        new_version = f"{major}.{minor}.{patch}"

        # Update evolution state
        db.table("system_evolution").update({
            "personality_version": new_version,
            "total_interactions": total_interactions,
            "total_users": total_users,
            "empathy_depth": round(empathy_depth, 4),
            "knowledge_breadth": round(knowledge_breadth, 4),
            "wisdom_score": round(wisdom_score, 4),
            "curiosity_level": round(curiosity_level, 4),
            "last_evolution_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }).eq("id", 1).execute()

        logger.info(
            "evolution_engine_cycle_complete",
            version=new_version,
            interactions=total_interactions,
            users=total_users,
            empathy=round(empathy_depth, 4),
            knowledge=round(knowledge_breadth, 4),
            wisdom=round(wisdom_score, 4),
        )

    except Exception as e:
        logger.error("evolution_engine_cycle_error", error=str(e))
