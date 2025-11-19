# RAG Voice Bot (Gemini embeddings + Weaviate Cloud Service)

This repository contains a full-stack RAG voice bot:
- Backend: FastAPI, Google Gemini embeddings (`models/text-embedding-004`), Weaviate Cloud Service (WCS)
- Frontend: React + Vite (voice & text chat, document upload)
- When the user uploads a document it is vectorized and stored in Weaviate.
- Queries are answered **only** from the uploaded document. If no relevant content is found the bot replies: "I don't have enough information to answer this from the uploaded document."

---

## Requirements

- Python 3.11+ (backend)
- Node.js 18+ (frontend)
- Weaviate Cloud Service account + API key
- Google Gemini API key

---

## Setup — Backend

1. Copy env:
```bash
cd backend
cp .env.example .env
# edit .env with your keys:
# GEMINI_API_KEY, WEAVIATE_URL, WEAVIATE_API_KEY
