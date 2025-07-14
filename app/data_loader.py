# app/data_loader.py

import json
from app.vector_store import VectorStore
from app.utils import chunk_text

# === Load pre-cleaned vehicle data and embed ===
def load_vehicle_data():
    with open("app/data/vehicles.json", "r", encoding="utf-8") as f:
        vehicles = json.load(f)

    chunks = []
    for vehicle in vehicles:
        name = vehicle.get("name", "Unnamed")
        description = vehicle.get("description", "")
        if not description:
            continue

        for chunk in chunk_text(description):
            chunks.append({
                "text": chunk,
                "metadata": {
                    "name": name,
                    "type": vehicle.get("type", ""),
                    "source": "vehicle"
                }
            })

    vstore = VectorStore()
    vstore.add_texts(chunks)
    vstore.save_local("app/embeddings/vehicles")

    return vstore, vehicles, chunks
