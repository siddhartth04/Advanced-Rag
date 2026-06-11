from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import hashlib


def chunk_documents(docs: list[Document], chunk_size: int = 800, overlap: int = 150) -> list[Document]:
    """Chunk documents using recursive character splitter with metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunked_docs = []
    chunk_id_counter = {}

    for doc in docs:
        source_file = doc.metadata.get("source_file", "unknown")
        doc_title = doc.metadata.get("doc_title", "unknown")

        if source_file not in chunk_id_counter:
            chunk_id_counter[source_file] = 0

        chunks = splitter.split_text(doc.page_content)

        for chunk_idx, chunk_text in enumerate(chunks):
            chunk_id_counter[source_file] += 1
            chunk_id = f"{source_file.replace('.md', '')}_{chunk_id_counter[source_file]:03d}"

            chunk_hash = hashlib.sha256(chunk_text.encode()).hexdigest()[:8]

            chunked_doc = Document(
                page_content=chunk_text,
                metadata={
                    "source_file": source_file,
                    "doc_title": doc_title,
                    "chunk_id": chunk_id,
                    "chunk_hash": chunk_hash,
                    "char_start": 0,
                    "section_header": extract_section_header(chunk_text),
                },
            )
            chunked_docs.append(chunked_doc)

    return chunked_docs


def extract_section_header(text: str) -> str:
    """Extract the first heading from text as section header."""
    lines = text.split("\n")
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("#").strip()
    return "Untitled Section"
