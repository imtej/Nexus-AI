"""
Nexus AI — Evolution API Routes
Public endpoints for System's evolution stats.
"""

import structlog
from fastapi import APIRouter

from app.services.supabase_client import get_supabase_admin
from app.models.evolution import EvolutionStats, SystemEvolution

logger = structlog.get_logger()

router = APIRouter(prefix="/evolution", tags=["evolution"])


@router.get("", response_model=EvolutionStats)
async def get_evolution_stats():
    """Get System's current evolution stats. Public endpoint."""
    db = get_supabase_admin()

    try:
        result = db.table("system_evolution").select("*").eq("id", 1).single().execute()

        if not result.data:
            # Return default stats if not initialized
            return EvolutionStats(
                personality_version="1.0.0",
                evolution_stage="nascent",
                total_interactions=0,
                total_users=0,
                empathy_depth=0.1,
                knowledge_breadth=0.1,
                wisdom_score=0.1,
                curiosity_level=0.9,
                evolution_percentage=0.0,
            )

        evolution = SystemEvolution(**result.data)

        return EvolutionStats(
            personality_version=evolution.personality_version,
            evolution_stage=evolution.evolution_stage,
            total_interactions=evolution.total_interactions,
            total_users=evolution.total_users,
            empathy_depth=evolution.empathy_depth,
            knowledge_breadth=evolution.knowledge_breadth,
            wisdom_score=evolution.wisdom_score,
            curiosity_level=evolution.curiosity_level,
            evolution_percentage=evolution.evolution_percentage,
            last_evolution_at=evolution.last_evolution_at,
        )

    except Exception as e:
        logger.error("evolution_stats_error", error=str(e))
        return EvolutionStats(
            personality_version="1.0.0",
            evolution_stage="nascent",
            total_interactions=0,
            total_users=0,
            empathy_depth=0.1,
            knowledge_breadth=0.1,
            wisdom_score=0.1,
            curiosity_level=0.9,
            evolution_percentage=0.0,
        )
