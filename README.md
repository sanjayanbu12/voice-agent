📘 Sanjay Bot — RAG Voice Assistant

FastAPI + Weaviate Vector DB + Gemini 2.0 Flash + React + Vite

An intelligent voice-enabled chatbot that answers questions ONLY from user-uploaded documents (PDF/DOCX/TXT).
It uses a RAG (Retrieval-Augmented Generation) pipeline with Weaviate + Gemini 2.0.

✨ Features

📄 Upload PDF / DOCX / TXT

🔍 Extracts text + Chunks + Embeds (Gemini text-embedding-004)

🧠 Stores vectors inside Weaviate Cloud

🤖 Queries Gemini 2.0 Flash using ONLY retrieved chunks

🎤 Voice input & voice output

🔁 Reset system to delete all documents

⚡ FastAPI backend + React frontend

💬 Chat UI + RAG pipeline


⚙️ Setup Instructions

🧩 1. Backend Setup (FastAPI)
Install dependencies:
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

🟦 2. Create .env inside backend/
GEMINI_API_KEY="your_gemini_key"

WEAVIATE_URL="https://your-cluster.weaviate.network"
WEAVIATE_API_KEY="your_weaviate_key"

API_HOST=0.0.0.0
API_PORT=8000

▶️ 3. Start Backend
uvicorn app.main:app --reload


Backend runs at:

👉 http://localhost:8000

🟩 4. Frontend Setup (React + Vite)
cd frontend
npm install

Create frontend/.env:
VITE_API_BASE_URL="http://localhost:8000"

Start frontend
npm run dev


Frontend runs at:

👉 http://localhost:5173

🧠 RAG Pipeline Explained
1. User uploads PDF/DOCX/TXT

→ Backend extracts text

2. chunk_text()

→ Splits into overlapping chunks

3. embed_text()

→ Uses Gemini model: text-embedding-004

4. store_document()

→ Saves chunks + vectors into Weaviate

5. User asks a question

→ retrieve_similar(query) performs vector search

6. Gemini 2.0 Flash

→ Answers using ONLY retrieved chunks
→ If answer not found → returns fallback:

"I don't have enough information to answer this from the uploaded document."

🔁 Reset System

The reset button:

Deletes all vectors from Weaviate

Deletes uploads folder

Recreates schema

Clears UI