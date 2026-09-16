from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from app.core.config import settings
from app.modules.knowledge.embeddings import get_embeddings


def get_qdrant_client() -> QdrantClient:
    if settings.qdrant_api_key:
        return QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )

    return QdrantClient(url=settings.qdrant_url)


def ensure_collection() -> None:
    client = get_qdrant_client()

    collections = client.get_collections()

    existing_collections = [
        collection.name
        for collection in collections.collections
    ]

    if settings.qdrant_collection in existing_collections:
        return

    embeddings = get_embeddings()

    vector_size = len(
        embeddings.embed_query("Premium Design Consultancy")
    )

    client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def get_vector_store() -> QdrantVectorStore:
    ensure_collection()

    client = get_qdrant_client()
    embeddings = get_embeddings()

    return QdrantVectorStore(
        client=client,
        collection_name=settings.qdrant_collection,
        embedding=embeddings,
    )