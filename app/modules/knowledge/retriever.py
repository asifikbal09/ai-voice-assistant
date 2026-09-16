from app.modules.knowledge.vector_store import get_vector_store


DEFAULT_SCORE_THRESHOLD = 0.35


def get_relevant_documents(
    query: str,
    k: int = 4,
    score_threshold: float = DEFAULT_SCORE_THRESHOLD,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    relevant_documents = []

    for document, score in results:
        if score >= score_threshold:
            relevant_documents.append(document)

    return relevant_documents


def search_with_scores(
    query: str,
    k: int = 4,
):
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(
        query,
        k=k,
    )

    return [
        {
            "score": float(score),
            "content": document.page_content,
            "metadata": document.metadata,
        }
        for document, score in results
    ]