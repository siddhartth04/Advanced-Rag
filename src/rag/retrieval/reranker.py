from sentence_transformers import CrossEncoder


class CrossEncoderReranker:
    """Singleton cross-encoder for reranking. """

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._model is None:
            self._model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    def rerank(self, query: str, documents: list[str], top_k: int = 4) -> list[tuple[int, float]]:
        """Rerank documents using cross-encoder.

        Args:
            query: query string
            documents: list of document texts
            top_k: return top K results

        Returns:
            list of (index, score) tuples sorted by score descending
        """
        if not documents:
            return []

        # Score all (query, document) pairs
        pairs = [[query, doc] for doc in documents]
        scores = self._model.predict(pairs)

        # Sort by score and return top-k
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]
