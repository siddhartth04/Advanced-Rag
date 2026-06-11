from rag.llm import call_llm_json


async def route_query(query: str) -> str:
    """Route query to appropriate strategy based on classification.

    Returns:
        One of: "chitchat", "factual", "multi_hop", "summarization"
    """
    prompt = f"""Classify the following user question into one of these categories:

1. "chitchat": casual, off-topic, or doesn't need information retrieval (e.g., "What's the weather?", "Tell me a joke")
2. "factual": straightforward question that needs specific information (e.g., "What is Axonify's ARR?")
3. "multi_hop": requires multiple pieces of information or reasoning across documents (e.g., "Which ADR addressed the issue mentioned in the postmortem?")
4. "summarization": asks for a summary or overview of information (e.g., "Summarize Q3 performance")

User Question: {query}

Respond with ONLY a JSON object like {{"route": "factual"}}"""

    messages = [{"role": "user", "content": prompt}]

    try:
        result = await call_llm_json(messages)
        route = result.get("route", "factual")
        if route not in ["chitchat", "factual", "multi_hop", "summarization"]:
            route = "factual"
        return route
    except Exception:
        return "factual"
