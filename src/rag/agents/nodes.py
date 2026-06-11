from langchain_core.documents import Document
from rag.llm import call_llm, call_llm_json, stream_llm
from rag.retrieval.router import route_query
from rag.retrieval.embedder import SentenceTransformerEmbedder
from rag.agents.state import GraphState
from rag.agents.prompts import (
    DECOMPOSE_QUERY_PROMPT,
    GRADE_DOCUMENTS_PROMPT,
    TRANSFORM_QUERY_PROMPT,
    GENERATE_PROMPT,
    GRADE_GENERATION_PROMPT,
    CHITCHAT_PROMPT,
)


async def route_node(state: GraphState) -> GraphState:
    """Route query to appropriate strategy."""
    state["route"] = await route_query(state["question"])
    state["node_path"].append("route_query")
    return state


async def decompose_query_node(state: GraphState) -> GraphState:
    """Decompose multi-hop query into sub-questions."""
    prompt = DECOMPOSE_QUERY_PROMPT.format(question=state["question"])
    messages = [{"role": "user", "content": prompt}]
    try:
        result = await call_llm_json(messages)
        state["sub_questions"] = result.get("sub_questions", [state["question"]])
    except Exception:
        state["sub_questions"] = [state["question"]]
    state["node_path"].append("decompose_query")
    return state


async def retrieve_node(state: GraphState) -> GraphState:
    """Retrieve documents from Qdrant (placeholder)."""
    embedder = SentenceTransformerEmbedder()
    query = state["question"]
    embedding = embedder.embed_query(query)

    state["documents"] = [
        Document(
            page_content="Sample retrieved content",
            metadata={"source_file": "test.md", "chunk_id": "test_001"},
        )
    ]
    state["node_path"].append("retrieve")
    return state


async def grade_documents_node(state: GraphState) -> GraphState:
    """Grade retrieved documents for relevance."""
    relevant_docs = []
    for doc in state["documents"]:
        prompt = GRADE_DOCUMENTS_PROMPT.format(
            question=state["question"],
            document=doc.page_content[:500],
        )
        messages = [{"role": "user", "content": prompt}]
        try:
            result = await call_llm_json(messages)
            if result.get("grade") == "yes":
                relevant_docs.append(doc)
        except Exception:
            relevant_docs.append(doc)

    state["documents"] = relevant_docs
    state["node_path"].append("grade_documents")
    return state


async def transform_query_node(state: GraphState) -> GraphState:
    """Transform query for better retrieval."""
    prompt = TRANSFORM_QUERY_PROMPT.format(question=state["question"])
    messages = [{"role": "user", "content": prompt}]
    try:
        result = await call_llm_json(messages)
        state["question"] = result.get("new_question", state["question"])
    except Exception:
        pass
    state["node_path"].append("transform_query")
    return state


async def generate_node(state: GraphState) -> GraphState:
    """Generate answer from retrieved documents."""
    docs_text = "\n\n".join(
        [f"[{i+1}] {doc.page_content}" for i, doc in enumerate(state["documents"])]
    )
    prompt = GENERATE_PROMPT.format(
        question=state["original_question"],
        documents=docs_text,
    )
    messages = [{"role": "user", "content": prompt}]
    state["generation"] = await call_llm(messages)
    state["node_path"].append("generate")
    return state


async def grade_generation_node(state: GraphState) -> GraphState:
    """Grade generated answer for hallucination and relevance."""
    prompt = GRADE_GENERATION_PROMPT.format(
        question=state["original_question"],
        answer=state["generation"],
    )
    messages = [{"role": "user", "content": prompt}]
    try:
        result = await call_llm_json(messages)
        state["hallucination_grade"] = result.get("hallucination", "no")
        state["answer_grade"] = result.get("relevance", "yes")
    except Exception:
        state["hallucination_grade"] = "no"
        state["answer_grade"] = "yes"
    state["node_path"].append("grade_generation")
    return state


async def generate_direct_node(state: GraphState) -> GraphState:
    """Generate answer for chitchat without retrieval."""
    prompt = CHITCHAT_PROMPT.format(question=state["question"])
    messages = [{"role": "user", "content": prompt}]
    state["generation"] = await call_llm(messages)
    state["node_path"].append("generate_direct")
    return state


def should_retrieve(state: GraphState) -> bool:
    """Determine if retrieval is needed."""
    return state["route"] in ["factual", "multi_hop", "summarization"]


def should_transform(state: GraphState) -> bool:
    """Determine if query transformation is needed (no relevant docs)."""
    return len(state["documents"]) == 0 and state["retries"] < 2


def should_regenerate(state: GraphState) -> bool:
    """Determine if regeneration is needed (hallucination or irrelevance)."""
    return (
        (state["hallucination_grade"] == "yes" or state["answer_grade"] == "no")
        and state["retries"] < 2
    )


def should_end(state: GraphState) -> bool:
    """Determine if graph should end."""
    return (
        state["hallucination_grade"] == "no"
        and state["answer_grade"] == "yes"
        or state["retries"] >= 2
    )
