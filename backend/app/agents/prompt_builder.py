"""
Nexus AI — Node 3: PromptBuilder Agent
Constructs the dynamic system prompt with personality, memories, and context.
"""

import structlog
import yaml
from pathlib import Path

from app.agents.state import WorkflowState
from app.services.supabase_client import get_supabase_admin

logger = structlog.get_logger()

# Load personality config
_personality_config = None


def _get_personality_config() -> dict:
    """Load and cache the personality YAML config."""
    global _personality_config
    if _personality_config is None:
        config_path = Path(__file__).parent.parent / "config" / "system_personality.yaml"
        with open(config_path, "r") as f:
            _personality_config = yaml.safe_load(f)
    return _personality_config


def _get_evolution_modifier(total_interactions: int) -> str:
    """Get personality modifier based on evolution stage."""
    config = _get_personality_config()
    stages = config["system"]["evolution_stages"]

    if total_interactions >= 10000:
        return stages["transcendent"]["personality_modifier"]
    elif total_interactions >= 1000:
        return stages["mature"]["personality_modifier"]
    elif total_interactions >= 100:
        return stages["growing"]["personality_modifier"]
    return stages["nascent"]["personality_modifier"]


async def prompt_builder_node(state: WorkflowState) -> dict:
    """Node 3 — Build the dynamic system prompt."""
    logger.info("prompt_builder_start", user_id=state.user_id)

    config = _get_personality_config()

    # Get System's evolution state
    db = get_supabase_admin()
    try:
        evolution_result = db.table("system_evolution").select("*").eq("id", 1).single().execute()
        evolution = evolution_result.data or {}
    except Exception:
        evolution = {"total_interactions": 0}

    total_interactions = evolution.get("total_interactions", 0)

    # Build prompt sections
    sections = []

    # 1. Core personality
    sections.append(config["system"]["core_personality"])

    # 2. Evolution modifier
    evolution_modifier = _get_evolution_modifier(total_interactions)
    sections.append(f"\n--- Current Evolution State ---\n{evolution_modifier}")

    # 3. User identity & Name
    if state.user_name or state.user_identity:
        identity_section = "\n--- About This Person ---\n"
        
        # Inject the name unconditionally if available
        if state.user_name:
            identity_section += f"Name: {state.user_name}\n"
            
        # Inject the deep psychology below it
        if state.user_identity:
            if state.user_identity.identity_summary:
                identity_section += f"Psychological Summary: {state.user_identity.identity_summary}\n"
            if state.user_identity.communication_style:
                identity_section += f"Communication preference: {state.user_identity.communication_style}\n"
            if state.user_identity.emotional_baseline:
                identity_section += f"Emotional baseline: {state.user_identity.emotional_baseline}\n"
            if state.user_identity.traits:
                traits_str = ", ".join(
                    f"{k}: {v}" for k, v in state.user_identity.traits.items()
                )
                identity_section += f"Known traits: {traits_str}\n"
        
        sections.append(identity_section)

    # 4. Personal memories
    if state.personal_memories:
        memory_section = "\n--- Your Memories of This Person ---\n"
        for i, mem_result in enumerate(state.personal_memories[:5], 1):
            mem = mem_result.memory
            memory_section += f"{i}. [{mem.memory_type}] {mem.content}\n"
        sections.append(memory_section)

    # 5. Collective knowledge insights
    if state.collective_knowledge:
        hive_section = "\n--- Collective Knowledge Base ---\n"
        for i, insight in enumerate(state.collective_knowledge[:3], 1):
            hive_section += f"{i}. [{insight.category}] {insight.content}\n"
        sections.append(hive_section)

    # 6. Emotional context
    if state.emotion_signal and state.emotion_signal != "neutral":
        sections.append(
            f"\n--- Current Emotional Context ---\n"
            f"The person seems to be feeling: {state.emotion_signal}. "
            f"Respond with appropriate emotional awareness."
        )

    # 7. Conversational Intent
    if state.intent and state.intent not in ("other", "casual_chat"):
        intent_rules = {
            "venting": "The user is venting. Prioritize listening and validating their feelings over offering immediate solutions.",
            "seeking_advice": "The user is explicitly seeking advice. Offer thoughtful, balanced, and non-judgmental guidance.",
            "deep_conversation": "The user wants a deep conversation. Match their philosophical depth and engage reflectively.",
        }
        
        rule = intent_rules.get(state.intent, f"The user's primary intent is: {state.intent}. Align your response to serve this intent.")
        sections.append(
            f"\n--- Actionable Intent ---\n"
            f"{rule}"
        )

    system_prompt = "\n".join(sections)

    logger.info(
        "prompt_builder_complete",
        prompt_length=len(system_prompt),
        has_identity=state.user_identity is not None,
        memory_count=len(state.personal_memories),
        collective_count=len(state.collective_knowledge),
    )

    return {"system_prompt": system_prompt}
