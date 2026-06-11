from pathlib import Path
from langchain_core.documents import Document


async def load_markdown_files(directory: str | Path) -> list[Document]:
    """Load all markdown files from directory."""
    directory = Path(directory)
    docs = []

    for file_path in sorted(directory.glob("*.md")):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        doc = Document(
            page_content=content,
            metadata={
                "source_file": file_path.name,
                "doc_title": file_path.stem.replace("_", " ").title(),
            },
        )
        docs.append(doc)

    return docs
