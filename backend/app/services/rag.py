import os
import uuid
import traceback
from typing import List
from ..config import settings
from .weaviate_client import get_client, ensure_schema
from .embeddings import embed_text
from .extractor import extract_text, chunk_text

def _get_client_and_class():
    client, class_name = ensure_schema()
    return client, class_name


def store_document(file_path: str, doc_id: str = None):
    """
    Extracts text, chunks, gets embeddings, stores objects in Weaviate with vectors.
    Returns number of chunks stored and doc_id.
    """
    try:
        if doc_id is None:
            doc_id = str(uuid.uuid4())

        text = extract_text(file_path)
        if not text or not text.strip():
            raise ValueError("No text extracted from document.")

        chunks: List[str] = chunk_text(text, chunk_size=500, overlap=50)
        if not chunks:
            raise ValueError("Chunking produced zero chunks.")

        client, CLASS_NAME = _get_client_and_class()

        objects_added = 0

        with client.batch as batch:
            batch.batch_size = 20
            for idx, chunk in enumerate(chunks):
                if not chunk or not chunk.strip():
                    continue 

                try:
                    emb = embed_text(chunk)
                except Exception as e:
                    print("Embedding failed for a chunk — skipping. Error:", e)
                    traceback.print_exc()
                    continue

                properties = {
                    "text": chunk,
                    "doc_id": doc_id,
                    "chunk_index": idx,
                    "meta": f"source:{os.path.basename(file_path)}",
                }

                batch.add_data_object(properties, CLASS_NAME, vector=emb)
                objects_added += 1

        return {"doc_id": doc_id, "chunks": objects_added}
    except Exception as e:
        print("store_document error:", e)
        traceback.print_exc()
        raise


def retrieve_similar(query: str, top_k: int = 3, score_threshold: float = 0.5):
    """
    Embed query then run Weaviate nearVector search. Returns simplified list of results.
    """
    try:
        client, CLASS_NAME = _get_client_and_class()

        q_emb = embed_text(query)
        near_vector = {"vector": q_emb}

        res = client.query.get(CLASS_NAME, ["text", "doc_id", "chunk_index", "_additional {id, vector, distance}"])\
                .with_near_vector(near_vector)\
                .with_limit(top_k)\
                .do()

        data = []
        try:
            objs = res.get("data", {}).get("Get", {}).get(CLASS_NAME, [])
        except Exception:
            objs = []

        for o in objs:
            text = o.get("text")
            add = o.get("_additional", {})
            distance = add.get("distance")
            obj_id = add.get("id")
            data.append({"id": obj_id, "text": text, "distance": distance})

        return data
    except Exception as e:
        print("retrieve_similar error:", e)
        traceback.print_exc()
        return []
