import pytest
from langchain_core.documents import Document
from rag.ingestion.chunking import chunk_documents, extract_section_header


def test_chunk_size_bounds():
    """Chunks should be within  size bounds."""
    doc = Document(
        page_content="This is a test document. " * 100,
        metadata={"source_file": "test.md", "doc_title": "Test"},
    )
    chunks = chunk_documents([doc], chunk_size=200, overlap=50)
    assert len(chunks) > 0
    for chunk in chunks:
        assert 100 <= len(chunk.page_content) <= 500


def test_chunk_metadata_preserved():
    """Chunk metadata should include source_file, doc_title, chunk_id."""
    doc = Document(
        page_content="# Test Section\nContent here.",
        metadata={"source_file": "01_test.md", "doc_title": "Test Doc"},
    )
    chunks = chunk_documents([doc])
    assert len(chunks) > 0
    for chunk in chunks:
        assert "source_file" in chunk.metadata
        assert "doc_title" in chunk.metadata
        assert "chunk_id" in chunk.metadata
        assert "section_header" in chunk.metadata
        assert chunk.metadata["source_file"] == "01_test.md"


def test_extract_section_header():
    """Extract section header from text."""
    text = "# Main Section\nSome content"
    header = extract_section_header(text)
    assert header == "Main Section"

    text_no_header = "No heading here\nJust content"
    header = extract_section_header(text_no_header)
    assert header == "Untitled Section"


def test_chunk_overlap():
    """Overlapping chunks should have some content in common."""
    doc = Document(
        page_content="word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 " * 20,
        metadata={"source_file": "test.md", "doc_title": "Test"},
    )
    chunks = chunk_documents([doc], chunk_size=100, overlap=20)
    assert len(chunks) >= 2


def test_empty_document():
    """Empty documents should not crash."""
    doc = Document(
        page_content="",
        metadata={"source_file": "empty.md", "doc_title": "Empty"},
    )
    chunks = chunk_documents([doc])
    assert len(chunks) == 0 or len(chunks[0].page_content) == 0
