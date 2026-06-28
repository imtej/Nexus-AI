"""
Nexus AI — Node 4: ResponseGenerator Agent
Generates the LLM response using the dynamic system prompt.
"""
###### Due to real hardware level chat streaming here, this file is not used for node 4 response generator #######
###### That's why it is directly implemented in chat.py file #######


import structlog
from app.agents.state import WorkflowState
from app.services.llm_service import LLMService

logger = structlog.get_logger()


async def response_generator_node(state: WorkflowState) -> dict:
    """Node 4 — Generate the response using the complete system prompt."""
    logger.info("response_generator_start", user_id=state.user_id)

    if not state.system_prompt:
        logger.error("response_generator_no_prompt")
        return {"response": "I'm having trouble gathering my thoughts. Could you try again?"}

    llm = LLMService(
        provider=state.llm_provider,
        api_key=state.llm_api_key or "",
    )

    # Build message list from conversation history + current message
    messages = []
    for msg in state.conversation_history[-10:]:  # Last 10 messages for context
        messages.append({
            "role": msg.get("role", "user"),
            "content": msg.get("content", ""),
        })
    messages.append({"role": "user", "content": state.user_message})

    try:
        response = await llm.generate(
            system_prompt=state.system_prompt,
            messages=messages,
        )

        logger.info("response_generator_complete", response_length=len(response))
        return {"response": response}

    except Exception as e:
        logger.error("response_generator_error", error=str(e))
        return {
            "response": "I'm having a moment — something went wrong on my end. Please try again after some time.",
            "error": str(e),
        }
