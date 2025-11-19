import os
import shutil
import asyncio
import traceback
import aiofiles
import uvicorn

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .models import ChatRequest
from .services import rag


print("LOADED FROM ENV:", settings.WEAVIATE_URL)

app = FastAPI(title="RAG Voice Bot Backend")

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "RAG Voice Bot Backend is running."}



@app.post("/api/upload")
async def upload_endpoint(file: UploadFile = File(...)):
    try:
        filename = file.filename
        if not filename:
            raise HTTPException(status_code=400, detail="No filename provided")

        dest = os.path.join(UPLOAD_DIR, filename)

        async with aiofiles.open(dest, "wb") as f:
            await f.write(await file.read())

        result = await asyncio.to_thread(rag.store_document, dest)

        return {
            "message": "uploaded",
            "doc_id": result["doc_id"],
            "chunks": result["chunks"],
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Upload failed, see server logs.")



@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        query = req.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        
        sims = await asyncio.to_thread(rag.retrieve_similar, query, 3, 0.5)

        if not sims:
            return {
                "response": "I don't have enough information to answer this from the uploaded document."
            }

        
        context_texts = "\n\n".join(
            [f"- {s['text']}" for s in sims if s.get("text") and s["text"].strip()]
        )

        prompt = f"""
Use ONLY the following document contents to answer the user's question.
If the answer is not present in the content, reply exactly:
"I don't have enough information to answer this from the uploaded document."

Document Content:
{context_texts}

User Question:
{query}

Answer in 2–4 sentences.
"""

        
        def gen_text():
            import google.generativeai as genai

            genai.configure(api_key=settings.GEMINI_API_KEY)

            model = genai.GenerativeModel("gemini-2.0-flash")

            try:
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": 300},
                )
                return response.text
            except Exception as e:
                print("Gemini generation failed:", e)
                raise

        answer = await asyncio.to_thread(gen_text)

        if not answer:
            return {
                "response": "I don't have enough information to answer this from the uploaded document."
            }

        return {"response": answer.strip()}

    except HTTPException:
        raise

    except Exception as e:
        print("CHAT ERROR:", e)
        traceback.print_exc()
        return {"response": "Sorry, something went wrong while generating the answer."}



if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
