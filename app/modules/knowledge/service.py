from app.modules.knowledge.loader import load_markdown_documents
from app.modules.knowledge.splitter import split_documents
from app.modules.knowledge.vector_store import get_vector_store
from app.modules.knowledge.retriever import get_relevant_documents


def test_document_processing():
    documents = load_markdown_documents()
    chunks = split_documents(documents)

    return {
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
        "documents": [
            {
                "source": document.metadata.get("source"),
                "category": document.metadata.get("category"),
            }
            for document in documents
        ],
        "chunks_preview": [
            {
                "content": chunk.page_content[:200],
                "metadata": chunk.metadata,
            }
            for chunk in chunks[:5]
        ],
    }


def ingest_knowledge():
    # 1. Load documents
    documents = load_markdown_documents()

    # 2. Split documents into chunks
    chunks = split_documents(documents)

    if not chunks:
        return {
            "success": False,
            "message": "No knowledge documents found.",
            "documents_loaded": len(documents),
            "chunks_created": 0,
        }

    # 3. Get Qdrant vector store
    vector_store = get_vector_store()

    # 4. Generate embeddings and store in Qdrant
    vector_store.add_documents(chunks)

    return {
        "success": True,
        "message": "Knowledge successfully ingested into Qdrant.",
        "documents_loaded": len(documents),
        "chunks_created": len(chunks),
    }
    

def search_knowledge(query: str):
    documents = get_relevant_documents(query)

    return {
        "success": True,
        "query": query,
        "results": [
            {
                "content": document.page_content,
                "metadata": document.metadata,
            }
            for document in documents
        ],
    }
    
    
from app.modules.knowledge.retriever import search_with_scores


def debug_knowledge_search(query: str):
    results = search_with_scores(query)

    return {
        "success": True,
        "query": query,
        "results": results,
    }