import pytest


@pytest.mark.asyncio
async def test_route_factual(mock_litellm):
    """Route factual queries correctly."""
    from rag.retrieval.router import route_query

    mock_response = mock_litellm.return_value
    mock_response.choices = [mock_response.choices[0]]
    mock_response.choices[0].message.content = '{"route": "factual"}'

    result = await route_query("What is Axonify's ARR?")
    assert result == "factual"


@pytest.mark.asyncio
async def test_route_multi_hop(mock_litellm):
    """Route multi-hop queries correctly."""
    from rag.retrieval.router import route_query

    mock_response = mock_litellm.return_value
    mock_response.choices = [mock_response.choices[0]]
    mock_response.choices[0].message.content = '{"route": "multi_hop"}'

    result = await route_query("Which incident is mentioned in the ADR?")
    assert result == "multi_hop"


@pytest.mark.asyncio
async def test_route_fallback(mock_litellm):
    """Route should fallback to factual on error."""
    from rag.retrieval.router import route_query

    mock_response = mock_litellm.return_value
    mock_response.choices = [mock_response.choices[0]]
    mock_response.choices[0].message.content = 'invalid json'

    result = await route_query("Some query")
    assert result == "factual"
