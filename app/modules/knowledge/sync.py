from app.modules.knowledge.loader import load_markdown_documents
from app.modules.knowledge.splitter import split_documents
from app.modules.knowledge.ids import generate_chunk_id
from app.modules.knowledge.vector_store import get_qdrant_client
from app.modules.knowledge.embeddings import get_embeddings
from app.core.config import settings

from qdrant_client.models import PointStruct


def prepare_chunks():
    documents = load_markdown_documents()
    chunks = split_documents(documents)

    prepared = []

    source_chunk_counters = {}

    for chunk in chunks:
        source = chunk.metadata.get("source", "")

        chunk_index = source_chunk_counters.get(source, 0)
        source_chunk_counters[source] = chunk_index + 1

        chunk_id = generate_chunk_id(
            source=source,
            content=chunk.page_content,
            chunk_index=chunk_index,
        )

        chunk.metadata["chunk_index"] = chunk_index
        chunk.metadata["chunk_id"] = chunk_id

        prepared.append(
            {
                "id": chunk_id,
                "document": chunk,
            }
        )

    return prepared


def sync_knowledge():
    documents = load_markdown_documents()
    chunks = split_documents(documents)

    prepared_chunks = []

    source_chunk_counters = {}

    for chunk in chunks:
        source = chunk.metadata.get("source", "")

        chunk_index = source_chunk_counters.get(source, 0)
        source_chunk_counters[source] = chunk_index + 1

        chunk_id = generate_chunk_id(
            source=source,
            content=chunk.page_content,
            chunk_index=chunk_index,
        )

        chunk.metadata["chunk_index"] = chunk_index
        chunk.metadata["chunk_id"] = chunk_id

        prepared_chunks.append(
            {
                "id": chunk_id,
                "document": chunk,
            }
        )

    client = get_qdrant_client()
    embeddings = get_embeddings()

    from app.modules.knowledge.vector_store import ensure_collection

    ensure_collection()

    existing_points = client.scroll(
        collection_name=settings.qdrant_collection,
        limit=10000,
        with_payload=True,
        with_vectors=False,
    )[0]

    existing_ids = {
        str(point.id)
        for point in existing_points
    }

    new_ids = {
        chunk["id"]
        for chunk in prepared_chunks
    }

    points_to_upsert = []

    for chunk in prepared_chunks:
        document = chunk["document"]

        vector = embeddings.embed_query(
            document.page_content
        )

        points_to_upsert.append(
            PointStruct(
                id=chunk["id"],
                vector=vector,
                payload={
                    "page_content": document.page_content,
                    "metadata": document.metadata,
                },
            )
        )

    if points_to_upsert:
        client.upsert(
            collection_name=settings.qdrant_collection,
            points=points_to_upsert,
        )

    deleted_ids = existing_ids - new_ids

    if deleted_ids:
        client.delete(
            collection_name=settings.qdrant_collection,
            points_selector=list(deleted_ids),
        )

    return {
        "success": True,
        "documents_loaded": len(documents),
        "chunks_created": len(prepared_chunks),
        "chunks_upserted": len(points_to_upsert),
        "chunks_deleted": len(deleted_ids),
    }