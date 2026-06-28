"""
Nexus AI — Node 1: QueryAnalyzer Agent
From the user message, detects user intent, emotional signals, and generates an expanded search query for vector database.
"""

import json
import structlog
from pydantic import BaseModel, Field
from app.agents.state import WorkflowState
from app.services.llm_service import LLMService

logger = structlog.get_logger()

class QueryAnalysis(BaseModel):
    intent: str = Field(description="The primary intent. One of: greeting, question, sharing, venting, seeking_advice, casual_chat, deep_conversation, farewell, other")
    emotion: str = Field(description="The emotional signal. One of: happy, sad, anxious, excited, neutral, frustrated, curious, grateful, nostalgic, vulnerable")
    search_query: str = Field(description="A highly optimized vector search string expanding the user's message using conversation context to fetch relevant database memories.")

INTENT_PROMPT = """Analyze the user's latest message using the context of the recent conversation history.
Extract their intent, emotional signal, and generate an expanded search query.

Recent Conversation History:
{history}

User message: "{message}"

The 'search_query' MUST transform their message into a highly detailed semantic vector search string. 
For example, if the user says "yeah tell me more about it", the search query should be "User wants to hear more about [The Topic Discussed Above]".
If the message is just a standalone greeting like "hi", the search query can just be "greeting"."""


async def query_analyzer_node(state: WorkflowState) -> dict:
    """Node 1 — Detect intent and emotion from user message."""
    logger.info("query_analyzer_start", user_id=state.user_id)

    try:
        llm = LLMService(
            provider=state.llm_provider,
            api_key=state.llm_api_key or "",
        )

        # Format chat history for context
        history_text = "No prior history."
        if state.conversation_history:
            history_text = "\n".join(
                f"{msg['role'].capitalize()}: {msg['content']}"
                for msg in state.conversation_history[-4:]  # Last 4 messages
            )

        prompt = INTENT_PROMPT.format(history=history_text, message=state.user_message)
        
        # Pydantic Structured Output handles all JSON formatting and extraction flawlessly
        analysis = await llm.fast_extract(prompt, schema=QueryAnalysis)

        logger.info(
            "query_analyzer_complete", 
            intent=analysis.intent, 
            emotion=analysis.emotion,
            search_query=analysis.search_query
        )
        return {
            "intent": analysis.intent, 
            "emotion_signal": analysis.emotion,
            "search_query": analysis.search_query
        }

    except Exception as e:
        logger.warning("query_analyzer_fallback", error=str(e))
        return {
            "intent": "other", 
            "emotion_signal": "neutral",
            "search_query": state.user_message
        }
