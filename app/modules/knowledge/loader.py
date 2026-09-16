from pathlib import Path

from langchain_core.documents import Document


KNOWLEDGE_DIR = Path("knowledge")


def load_markdown_documents() -> list[Document]:
    documents = []

    for file_path in KNOWLEDGE_DIR.rglob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        if not content.strip():
            continue

        category = file_path.parent.name

        documents.append(
            Document(
                page_content=content,
                metadata={
                    "source": str(file_path),
                    "category": category,
                    "filename": file_path.name,
                },
            )
        )

    return documents