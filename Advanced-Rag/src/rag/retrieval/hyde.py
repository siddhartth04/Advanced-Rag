from rag.llm import call_llm
from rag.retrieval.embedder import SentenceTransformerEmbedder


async def generate_hypothetical_document(query: str) -> str:
    """Use LLM to generate a hypothetical document that would answer the query."""
    prompt = f"""Write a 2–3 sentence factual passage that directly answers the following question.
Be specific and include concrete details.

Question: {query}

Passage:"""

    messages = [{"role": "user", "content": prompt}]
    response = await call_llm(messages)
    return response.strip()


async def hyde_embed(query: str) -> list[float]:
    """Generate hypothetical document and embed it for dense retrieval."""
    hypo_doc = await generate_hypothetical_document(query)
    embedder = SentenceTransformerEmbedder()
    embedding = embedder.embed_query(hypo_doc)
    return embedding
