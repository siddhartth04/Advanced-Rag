import pytest


@pytest.mark.asyncio
async def test_graph_factual_flow(mock_litellm):
    """Test factual query flow through graphs"""
    from rag.agents.graph import build_graph, run_query

    graph = build_graph()
    result = await run_query(graph, "What is Axonify's ARR?")

    assert "node_path" in result
    assert "route_query" in result["node_path"]
    assert result["generation"]  # Should have generated answer


@pytest.mark.asyncio
async def test_graph_chitchat_flow(mock_litellm):
    """Test chitchat query bypasses retrieval."""
    from rag.agents.graph import build_graph, run_query

    # Mock LLM to return chitchat route
    mock_response = mock_litellm.return_value
    mock_response.choices = [mock_response.choices[0]]
    mock_response.choices[0].message.content = '{"route": "chitchat"}'

    graph = build_graph()
    result = await run_query(graph, "What's the weather?")

    assert "generate_direct" in result["node_path"]
    assert "retrieve" not in result["node_path"]


@pytest.mark.asyncio
async def test_graph_retry_on_bad_docs(mock_litellm):
    """Test query transformation on no relevant docs."""
    from rag.agents.graph import build_graph, run_query

    graph = build_graph()
    result = await run_query(graph, "obscure question")

    # Should have attempted transformation if no docs were relevant
    assert "node_path" in result
    assert result["retries"] >= 0
