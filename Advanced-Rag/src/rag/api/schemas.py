from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    qdrant_connected: bool
    llm_model: str
    embed_model: str
    doc_count: int


class QueryRequest(BaseModel):
    question: str
    stream: bool = True


class Source(BaseModel):
    title: str
    source_file: str
    chunk_id: str
    score: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
    route: str
    confidence: str
    retries: int
    node_path: list[str]


class IngestRequest(BaseModel):
    paths: list[str]


class IngestResponse(BaseModel):
    chunks_indexed: int
    doc_count: int
    duration_s: float


class EvalResult(BaseModel):
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float
