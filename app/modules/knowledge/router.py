from fastapi import APIRouter

from app.core.config import settings
from app.modules.knowledge.vector_store import get_qdrant_client

from app.modules.knowledge.service import test_document_processing
from app.modules.knowledge.service import ingest_knowledge

from app.modules.knowledge.schemas import KnowledgeSearchRequest
from app.modules.knowledge.retriever import get_relevant_documents

from app.modules.knowledge.service import debug_knowledge_search

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"],
)


@router.get("/health")
async def knowledge_health():
    client = get_qdrant_client()

    collections = client.get_collections()

    return {
        "success": True,
        "qdrant": "connected",
        "collection": settings.qdrant_collection,
        "collections": [
            collection.name
            for collection in collections.collections
        ],
    }
    





@router.get("/documents-test")
async def documents_test():
    return test_document_processing()

#! Ingest knowledge documents into Qdrant vector store

@router.post("/ingest")
async def ingest():
    return ingest_knowledge()

# ! Search knowledge documents from Qdrant vector store

@router.post("/search")
async def search(request: KnowledgeSearchRequest):
    documents = get_relevant_documents(
        request.query,
        request.k,
    )

    return {
        "success": True,
        "query": request.query,
        "results": [
            {
                "content": document.page_content,
                "metadata": document.metadata,
            }
            for document in documents
        ],
    }
    
# ! Search knowledge documents with scores from Qdrant vector store
@router.post("/search-debug")
async def search_debug(request: KnowledgeSearchRequest):
    return debug_knowledge_search(request.query)


@router.get("/stats")
async def knowledge_stats():
    client = get_qdrant_client()

    collection = client.get_collection(
        settings.qdrant_collection
    )

    return {
        "success": True,
        "collection": settings.qdrant_collection,
        "vectors_count": collection.points_count,
    }
    
@router.post("/sync")
async def sync_knowledge():
    return ingest_knowledge()