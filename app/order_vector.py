# app/order_vector.py

import os
import json
import numpy as np
from app.vector_store import VectorStore
from app.embedder import get_embeddings
from app.utils import chunk_json_data

ORDER_JSON_PATH = "app/data/orders.json"
ORDER_EMBEDDINGS_PATH = "app/data/order_embeddings.npy"
ORDER_CHUNKS_PATH = "app/data/order_chunks.json"

def load_order_chunks():
    with open(ORDER_JSON_PATH, "r", encoding="utf-8") as f:
        orders = json.load(f)
    return chunk_json_data(orders)

def build_order_index(force_rebuild=False):
    chunks = load_order_chunks()

    if not force_rebuild and os.path.exists(ORDER_EMBEDDINGS_PATH) and os.path.exists(ORDER_CHUNKS_PATH):
        print("✅ Using cached order embeddings.")
        embeddings = np.load(ORDER_EMBEDDINGS_PATH)
        with open(ORDER_CHUNKS_PATH, "r", encoding="utf-8") as f:
            chunks = json.load(f)
    else:
        print("⚡ Generating embeddings for orders...")
        embeddings = get_embeddings(chunks)
        np.save(ORDER_EMBEDDINGS_PATH, embeddings)
        with open(ORDER_CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

    store = VectorStore(dim=len(embeddings[0]))
    store.add(embeddings, chunks)
    print(f"✅ Built index with {len(chunks)} chunks.")
    return store, chunks
