"""
Integration test for the LangGraph orchestrator state machine.
"""

import pytest

def test_langgraph_graph_initialization():
    from backend.app.agents.graph import create_nexus_graph

    graph = create_nexus_graph()
    assert graph is not None

    # Verify expected node graph structure
    nodes = list(graph.nodes.keys())
    assert "query_analyzer" in nodes
    assert "context_retriever" in nodes
    assert "prompt_builder" in nodes
    assert "response_generator" in nodes
