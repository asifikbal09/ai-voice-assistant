import hashlib
import uuid


def generate_chunk_id(
    source: str,
    content: str,
    chunk_index: int,
) -> str:
    raw_id = f"{source}:{chunk_index}:{content}"

    hash_value = hashlib.sha256(
        raw_id.encode("utf-8")
    ).hexdigest()

    return str(uuid.UUID(hash_value[:32]))