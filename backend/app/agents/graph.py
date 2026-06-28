"""
Nexus AI — LangGraph Workflow Definition
Orchestrates the 7 Agentic Nodes into a coherent workflow.
"""

import structlog
from langgraph.graph import StateGraph, END

from app.agents.state import WorkflowState
from app.agents.query_analyzer import query_analyzer_node
from app.agents.context_retriever import context_retriever_node
from app.agents.prompt_builder import prompt_builder_node
from app.agents.response_generator import response_generator_node

logger = structlog.get_logger()


def build_orchestration_graph() -> StateGraph:
    """Build the LangGraph workflow for the conversation pipeline.

    Flow:
        query_analyzer → context_retriever → prompt_builder → response_generator → memory_extractor → END

    Nodes 1-4 are in the critical path (sync).
    Node 5 (memory_extractor) runs after response generation.
    Nodes 6-7 (insight_distiller, evolution_engine) run as periodic background tasks, not in this graph.
    """

    graph = StateGraph(WorkflowState)

    # Add nodes
    graph.add_node("query_analyzer", query_analyzer_node)
    graph.add_node("context_retriever", context_retriever_node)
    graph.add_node("prompt_builder", prompt_builder_node)
    # graph.add_node("response_generator", response_generator_node)        ## Added generator with stream in directly chat.py

    # Define edges (linear flow)
    graph.set_entry_point("query_analyzer")
    graph.add_edge("query_analyzer", "context_retriever")
    graph.add_edge("context_retriever", "prompt_builder")
    # graph.add_edge("prompt_builder", "response_generator")      ## Added generator with stream in directly chat.py
    # graph.add_edge("response_generator", END)                  ## Added generator with stream in directly chat.py
    graph.add_edge("prompt_builder", END)

    return graph


# Compile the graph once at module load
_compiled_graph = None


def get_orchestration_graph():
    """Get the compiled workflow graph (cached)."""
    global _compiled_graph
    if _compiled_graph is None:
        graph = build_orchestration_graph()
        _compiled_graph = graph.compile()
        logger.info("orchestration_graph_compiled")
    return _compiled_graph
