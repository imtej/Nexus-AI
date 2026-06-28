"""
Nexus AI — Memory Service
Handles memory CRUD and vector search via Supabase pgvector.
"""

import structlog
from typing import Optional
from datetime import datetime

from app.models.memory import MemoryNode, MemoryNodeCreate, CollectiveKnowledgeInsight, MemorySearchResult
from app.services.supabase_client import get_supabase_admin
from app.services.embedding_service import generate_embedding, generate_query_embedding
from app.config.settings import get_settings

logger = structlog.get_logger()


class MemoryService:
    """Manages memory storage and retrieval."""

    def __init__(self):
        self.db = get_supabase_admin()
        self.settings = get_settings()

    async def store_memory(self, user_id: str, memory: MemoryNodeCreate) -> MemoryNode:
        """Store a new memory node with embedding."""
        try:
            # Generate embedding
            embedding = await generate_embedding(memory.content)

            # Insert into Supabase
            data = {
                "user_id": user_id,
                "content": memory.content,
                "memory_type": memory.memory_type,
                "tags": memory.tags,
                "embedding": embedding,
                "recency_score": 1.0,
                "importance_score": 0.5,
            }

            result = self.db.table("nexus_memory_nodes").insert(data).execute()

            if result.data:
                node_data = result.data[0]
                logger.info(
                    "memory_stored",
                    user_id=user_id,
                    memory_type=memory.memory_type,
                    memory_id=node_data["id"],
                )
                return MemoryNode(**node_data)

            raise Exception("Failed to store memory")

        except Exception as e:
            logger.error("memory_store_error", user_id=user_id, error=str(e))
            raise

    async def search_personal_memories(
        self,
        user_id: str,
        query: str,
        limit: int | None = None,
    ) -> list[MemorySearchResult]:
        """Search personal memories using vector similarity."""
        limit = limit or self.settings.personal_memory_limit

        try:
            query_embedding = await generate_query_embedding(query)

            # Use Supabase RPC for vector search
            result = self.db.rpc(
                "search_personal_memories",
                {
                    "query_embedding": query_embedding,
                    "target_user_id": user_id,
                    "match_count": limit,
                },
            ).execute()

            memories = []
            if result.data:
                for row in result.data:
                    memory = MemoryNode(
                        id=row["id"],
                        user_id=row["user_id"],
                        content=row["content"],
                        memory_type=row["memory_type"],
                        tags=row.get("tags", []),
                        recency_score=row.get("recency_score", 0.5),
                        importance_score=row.get("importance_score", 0.5),
                        created_at=row.get("created_at"),
                    )
                    memories.append(
                        MemorySearchResult(
                            memory=memory,
                            similarity_score=row.get("similarity", 0.0),
                        )
                    )

            logger.info(
                "personal_memories_searched",
                user_id=user_id,
                results=len(memories),
            )
            return memories

        except Exception as e:
            logger.error("personal_memory_search_error", user_id=user_id, error=str(e))
            return []

    async def search_collective_knowledge(
        self,
        query: str,
        limit: int | None = None,
    ) -> list[CollectiveKnowledgeInsight]:
        """Search Collective Knowledge memories using vector similarity."""
        limit = limit or self.settings.collective_knowledge_limit

        try:
            query_embedding = await generate_query_embedding(query)

            result = self.db.rpc(
                "search_collective_knowledge",
                {
                    "query_embedding": query_embedding,
                    "match_count": limit,
                },
            ).execute()

            insights = []
            if result.data:
                for row in result.data:
                    insights.append(
                        CollectiveKnowledgeInsight(
                            id=row["id"],
                            content=row["content"],
                            category=row["category"],
                            tags=row.get("tags", []),
                            contributor_count=row.get("contributor_count", 1),
                            quality_score=row.get("quality_score", 0.5),
                        )
                    )

            logger.info("collective_knowledge_searched", results=len(insights))
            return insights

        except Exception as e:
            logger.error("collective_knowledge_search_error", error=str(e))
            return []

    async def get_recent_memories(
        self,
        user_id: str,
        limit: int = 5,
    ) -> list[MemoryNode]:
        """Get recent memories as fallback when vector search yields few results."""
        try:
            result = (
                self.db.table("nexus_memory_nodes")
                .select("*")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )

            return [MemoryNode(**row) for row in (result.data or [])]

        except Exception as e:
            logger.error("recent_memory_fetch_error", user_id=user_id, error=str(e))
            return []

    async def get_user_identity(self, user_id: str) -> Optional[dict]:
        """Get the user's identity profile."""
        try:
            result = (
                self.db.table("nexus_user_identities")
                .select("*")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            return result.data
        except Exception:
            return None

    async def update_user_identity(self, user_id: str, identity_data: dict) -> None:
        """Upsert user identity."""
        try:
            identity_data["user_id"] = user_id
            identity_data["updated_at"] = datetime.utcnow().isoformat()

            self.db.table("nexus_user_identities").upsert(
                identity_data,
                on_conflict="user_id",
            ).execute()

            logger.info("user_identity_updated", user_id=user_id)
        except Exception as e:
            logger.error("user_identity_update_error", user_id=user_id, error=str(e))
