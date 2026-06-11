from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LiteLLM model string — change this to switch provider
    llm_model: str = "ollama/llama3.1:8b"
    llm_api_base: str | None = None
    llm_api_key: str | None = None

    # Embeddings (always local)
    embed_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embed_dim: int = 384

    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_collection: str = "axonify_docs"

    # LangSmith (optional)
    langchain_tracing_v2: bool = False
    langchain_api_key: str | None = None
    langchain_project: str = "multi-agent-rag"

    log_level: str = "INFO"
    cache_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
