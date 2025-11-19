import weaviate
from ..config import settings

def get_client():
    print("DEBUG WEAVIATE_URL =", settings.WEAVIATE_URL)  
    auth_config = weaviate.auth.AuthApiKey(api_key=settings.WEAVIATE_API_KEY)
    client = weaviate.Client(
        url=settings.WEAVIATE_URL,
        auth_client_secret=auth_config,
        additional_headers={
            "X-OpenAI-Api-Key": "",  # not used; keep empty
        }
    )
    return client

def ensure_schema():
    client = get_client()

    class_name = "DocumentChunk"

    existing = client.schema.get()

    classes = existing.get("classes", [])
    class_exists = any(c["class"] == class_name for c in classes)

    if not class_exists:
        schema = {
            "class": class_name,
            "vectorizer": "none",
            "properties": [
                {
                    "name": "text",
                    "dataType": ["text"],
                },
                {
                    "name": "doc_id",
                    "dataType": ["string"],
                },
                {
                    "name": "chunk_index",
                    "dataType": ["int"],
                },
                {
                    "name": "meta",
                    "dataType": ["text"],
                },
            ],
        }

        client.schema.create_class(schema)
        print(f"Created Weaviate class: {class_name}")
    else:
        print(f"Class already exists: {class_name}")

    return client, class_name

