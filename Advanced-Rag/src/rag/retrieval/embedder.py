from sentence_transformers import SentenceTransformer
from rag.config import settings


class SentenceTransformerEmbedder:
    """Singleton embedder using sentence-transformers."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._model = SentenceTransformer(settings.embed_model)

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query string."""
        embedding = self._model.encode(text, convert_to_tensor=False)
        return embedding.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of documents."""
        embeddings = self._model.encode(texts, convert_to_tensor=False)
        return embeddings.tolist()

    @property
    def embedding_dim(self) -> int:
        """Return embedding dimension."""
        return settings.embed_dim
