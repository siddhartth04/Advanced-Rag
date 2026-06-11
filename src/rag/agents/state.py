from typing import TypedDict
from langchain_core.documents import Document


class GraphState(TypedDict):
    """State dictionary for LangGraph multi-agent system."""

    question: str
    original_question: str
    route: str  # chitchat | factual | multi_hop | summarization
    sub_questions: list[str]  # for multi_hop decomposition
    documents: list[Document]
    generation: str
    retries: int  # max 2
    hallucination_grade: str  # yes | no
    answer_grade: str  # yes | no
    confidence: str  # high | low
    sources: list[dict]  # [{title, chunk_id, score, source_file}]
    node_path: list[str]
