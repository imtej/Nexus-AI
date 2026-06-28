"""
Nexus AI — Evolution Data Models
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SystemEvolution(BaseModel):
    """System's global evolution state (singleton)."""
    id: int = 1
    personality_version: str = "1.0.0"
    total_interactions: int = 0
    total_users: int = 0
    empathy_depth: float = 0.1
    knowledge_breadth: float = 0.1
    wisdom_score: float = 0.1
    curiosity_level: float = 0.9
    personality_md: Optional[str] = None
    last_evolution_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def evolution_stage(self) -> str:
        """Determine current evolution stage based on total interactions."""
        if self.total_interactions >= 10000:
            return "transcendent"
        elif self.total_interactions >= 1000:
            return "mature"
        elif self.total_interactions >= 100:
            return "growing"
        return "nascent"

    @property
    def evolution_percentage(self) -> float:
        """Calculate overall evolution as a percentage (0-100)."""
        # A true 0-100% aggregate score
        aggregate_decimal = (
            self.empathy_depth
            + self.knowledge_breadth
            + self.wisdom_score
            + (1.0 - self.curiosity_level)  # Decreased curiosity equals more maturity
        ) / 4.0
        
        return min(100.0, aggregate_decimal * 100.0)


class EvolutionStats(BaseModel):
    """Public-facing evolution stats for the dashboard."""
    personality_version: str
    evolution_stage: str
    total_interactions: int
    total_users: int
    empathy_depth: float
    knowledge_breadth: float
    wisdom_score: float
    curiosity_level: float
    evolution_percentage: float
    last_evolution_at: Optional[datetime] = None
