from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from rag.config import settings
from rag.retrieval.embedder import SentenceTransformerEmbedder
import uuid


async def index_documents(docs: list[Document]) -> int:
    """Index documents into Qdrant vector store."""
    client = QdrantClient(settings.qdrant_url)
    embedder = SentenceTransformerEmbedder()

    # Create or get collection
    try:
        client.get_collection(settings.qdrant_collection)
    except Exception:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(
                size=settings.embed_dim,
                distance=Distance.COSINE,
            ),
        )

    # Embed and index
    texts = [doc.page_content for doc in docs]
    embeddings = embedder.embed_documents(texts)

    points = []
    for doc, embedding in zip(docs, embeddings):
        point_id = uuid.uuid4().int % (2**63)
        point = PointStruct(
            id=point_id,
            vector=embedding,
            payload={
                "content": doc.page_content,
                "source_file": doc.metadata.get("source_file", ""),
                "doc_title": doc.metadata.get("doc_title", ""),
                "chunk_id": doc.metadata.get("chunk_id", ""),
                "section_header": doc.metadata.get("section_header", ""),
            },
        )
        points.append(point)

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
    )

    return len(points)
