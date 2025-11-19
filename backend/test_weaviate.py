from app.services.weaviate_client import get_client

client = get_client()

print("Checking schema...")
schema = client.schema.get()
print(schema)
