#!/usr/bin/env python3
"""Ingest sample documents into Qdrant."""

import asyncio
import sys
from pathlib import Path


# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rag.ingestion.loaders import load_markdown_files
from rag.ingestion.chunking import chunk_documents
from rag.ingestion.indexer import index_documents


async def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/ingest.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    print(f"Loading documents from {directory}...")
    docs = await load_markdown_files(directory)
    print(f"Loaded {len(docs)} documents")

    print("Chunking documents...")
    chunked_docs = chunk_documents(docs)
    print(f"Created {len(chunked_docs)} chunks")

    print("Indexing into Qdrant...")
    count = await index_documents(chunked_docs)
    print(f"Indexed {count} chunks successfully")


if __name__ == "__main__":
    asyncio.run(main())
