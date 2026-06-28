"""
Nexus AI — Embedding Service
Uses Gemini embeddings (768d) for all users, server-side.
"""

import structlog
from google import genai
from app.config.settings import get_settings

logger = structlog.get_logger()

_client = None


def _ensure_genai_configured():
    """Configure Google GenAI once."""
    global _client
    if _client is None:
        settings = get_settings()
        _client = genai.Client(api_key=settings.gemini_embedding_api_key)
        logger.info("genai_configured_for_embeddings")


async def generate_embedding(text: str) -> list[float]:
    """Generate a 768-dimension embedding vector for the given text."""
    _ensure_genai_configured()
    settings = get_settings()

    try:
        result = _client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
            config={'task_type': 'retrieval_document', 'output_dimensionality': settings.embedding_dimensions},
        )
        embedding = result.embeddings[0].values
        logger.debug("embedding_generated", dimensions=len(embedding))
        return embedding

    except Exception as e:
        logger.error("embedding_generation_error", error=str(e))
        raise


async def generate_query_embedding(text: str) -> list[float]:
    """Generate an embedding optimized for search queries."""
    _ensure_genai_configured()
    settings = get_settings()

    try:
        result = _client.models.embed_content(
            model=settings.embedding_model,
            contents=text,
            config={'task_type': 'retrieval_query', 'output_dimensionality': settings.embedding_dimensions},
        )
        return result.embeddings[0].values

    except Exception as e:
        logger.error("query_embedding_error", error=str(e))
        raise
