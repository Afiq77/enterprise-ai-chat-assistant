# app/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from tempfile import NamedTemporaryFile
from contextlib import asynccontextmanager
from datetime import datetime
import shutil
import os

from app.data_loader import load_vehicle_data
from app.gemini_wrapper import ask_model, generate_title_from_model, handle_voice_query
from app.order_loader import dump_orders_to_json
from app.order_vector import build_order_index
from app.rag_engine import RAGEngine


def custom_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


rag = None
raw_items = []
item_chunks = []

order_rag = None
order_chunks = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag, raw_items, item_chunks, order_rag, order_chunks

    print("⏳ Loading data...")

    rag, raw_items, item_chunks = load_vehicle_data()

    dump_orders_to_json()
    order_rag = RAGEngine()
    order_store, order_chunks = build_order_index()
    print("📦 Loading order chunks into vector store...")
    order_rag.vstore = order_store
    order_rag.is_loaded = True
    print("✅ RAG systems initialized.")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryInput(BaseModel):
    query: str

class QueryOutput(BaseModel):
    response: list[str]

class TitleRequest(BaseModel):
    message: str

class TitleResponse(BaseModel):
    title: str


@app.post("/chat", response_model=QueryOutput)
def chat(user_input: QueryInput):
    global rag, raw_items, item_chunks

    all_names = [item['name'] for item in raw_items]
    response = ask_model(user_input.query, item_chunks, raw_items, all_names)

    return {"response": [response]}


@app.post("/chat_order", response_model=QueryOutput)
def chat_order(user_input: QueryInput):
    global order_rag, order_chunks
    if not order_rag:
        return {"response": ["⚠️ Order module not loaded yet."]}
    response = order_rag.query(user_input.query)
    if not response:
        response = ["No matching records found."]
    return {"response": response}


@app.post("/generate_title", response_model=TitleResponse)
def generate_title(data: TitleRequest):
    title = generate_title_from_model(data.message)
    return {"title": title}


@app.post("/voice-query")
async def voice_query(file: UploadFile = File(...)):
    temp_path = None
    try:
        if not file.content_type.startswith("audio/"):
            return JSONResponse(status_code=400, content={"error": "Invalid file type."})

        with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        answer = handle_voice_query(temp_path)
        return {"response": answer}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Voice query failed: {str(e)}"})

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.post("/refresh")
def refresh_data():
    global rag, raw_items, item_chunks
    rag, raw_items, item_chunks = load_vehicle_data()
    return {"status": "refreshed", "total_items": len(raw_items)}
