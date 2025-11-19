import google.generativeai as genai
from ..config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def embed_text(text: str):
    """
    Embed using Gemini embeddings model (models/text-embedding-004).
    Returns a list[float]
    """
    resp = genai.embed_content(model="models/text-embedding-004", content=text)
    embedding = resp["embedding"]
    return embedding
