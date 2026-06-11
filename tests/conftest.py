import pytest
from unittest.mock import MagicMock, AsyncMock
from langchain_core.documents import Document
from qdrant_client import QdrantClient


@pytest.fixture
def mock_litellm(mocker):
    """Mock litellm.acompletion for deterministic testing."""
    async_mock = AsyncMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = '{"route": "factual"}'
    async_mock.return_value = mock_response
    mocker.patch("litellm.acompletion", async_mock)
    return async_mock


@pytest.fixture
def in_memory_qdrant():
    """Create an in-memory Qdrant client with pre-created collection."""
    client = QdrantClient(":memory:")
    client.create_collection(
        collection_name="axonify_docs",
        vectors_config={
            "dense": {
                "size": 384,
                "distance": "Cosine",
            }
        },
    )
    return client


@pytest.fixture
def sample_documents():
    """Return 5 sample Document objects with realistic Axonify content."""
    return [
        Document(
            page_content="Axonify Corp is a B2B SaaS platform founded in 2019 by Priya Mehta and James Okonkwo. "
            "The company provides AI-powered microlearning for enterprise customers.",
            metadata={
                "source_file": "01_company_overview.md",
                "doc_title": "Company Overview",
                "chunk_id": "chunk_001",
                "char_start": 0,
                "section_header": "Mission & Tagline",
            },
        ),
        Document(
            page_content="Axonify reached $42.1M ARR in Q3 2024 with 180 enterprise customers and 4.2M active learners.",
            metadata={
                "source_file": "01_company_overview.md",
                "doc_title": "Company Overview",
                "chunk_id": "chunk_002",
                "char_start": 250,
                "section_header": "Key Metrics",
            },
        ),
        Document(
            page_content="The Axonify Learn product uses an AI-driven Spaced Repetition Engine (SRE) to personalize question sequences. "
            "It supports 34 languages and WCAG 2.1 AA accessibility.",
            metadata={
                "source_file": "02_product_catalog.md",
                "doc_title": "Product Catalog",
                "chunk_id": "chunk_003",
                "char_start": 0,
                "section_header": "Product 1 — Axonify Learn",
            },
        ),
        Document(
            page_content="Encryption: AES-256 at rest on all databases and S3 buckets. In transit: TLS 1.3 enforced. "
            "Backups encrypted with customer-managed keys option on Enterprise tier.",
            metadata={
                "source_file": "04_security_compliance.md",
                "doc_title": "Security and Compliance",
                "chunk_id": "chunk_004",
                "char_start": 100,
                "section_header": "Encryption",
            },
        ),
        Document(
            page_content="The March 2024 incident (INC-2024-0312) was a P0 event lasting 5 hours 25 minutes. "
            "Root cause was a Kafka broker disk exhaustion from an infinite retry loop.",
            metadata={
                "source_file": "06_incident_postmortem.md",
                "doc_title": "Incident Postmortem",
                "chunk_id": "chunk_005",
                "char_start": 50,
                "section_header": "Incident Summary",
            },
        ),
    ]
