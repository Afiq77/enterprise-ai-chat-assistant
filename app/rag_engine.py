# app/rag_engine.py

import re
import numpy as np
from app.embedder import Embedder
from app.vector_store import VectorStore
from app.gemini_wrapper import ask_model
from app.order_formatter import format_order_record
from app.order_filter import filter_orders


class RAGEngine:
    def __init__(self):
        self.embedder = Embedder()
        self.vstore = VectorStore(dim=768)
        self.text_chunks = []
        self.is_loaded = False
        self.raw_orders = []

    def load_knowledge_base(self, chunks: list[str], raw_orders=None):
        if not chunks:
            raise ValueError("❌ No chunks to load into knowledge base.")
        embeddings = self.embedder.embed(chunks)
        self.vstore.add(embeddings, chunks)
        self.text_chunks = chunks
        self.is_loaded = True
        if raw_orders is not None:
            self.raw_orders = raw_orders

    def load_precomputed_knowledge_base(self, embeddings: np.ndarray, chunks: list[str], raw_orders=None):
        self.vstore.add(embeddings, chunks)
        self.text_chunks = chunks
        self.is_loaded = True
        if raw_orders is not None:
            self.raw_orders = raw_orders

    def extract_orderno(self, text: str) -> str | None:
        match = re.search(r"\bON\d{5,}\b", text.upper())
        return match.group(0) if match else None

    def query(self, user_query: str) -> list[str]:
        if not self.is_loaded:
            return ["⚠ Knowledge base not loaded yet."]

        # === Order query via order number pattern ===
        extracted_orderno = self.extract_orderno(user_query)
        if extracted_orderno:
            for chunk in self.text_chunks:
                fields = {
                    k.strip(): v.strip()
                    for part in chunk.split("||") if ":" in part
                    for k, v in [part.split(":", 1)]
                }
                if fields.get("orderno", "").lower() == extracted_orderno.lower():
                    return [ask_model(user_query, [chunk])]

            return [f"No order found with order number {extracted_orderno}"]

        # === Filter and summarize relevant orders ===
        if self.raw_orders:
            filtered, summary = filter_orders(self.raw_orders, user_query)
            if not filtered:
                return ["No orders matched your query."]
            top_formatted = "\n\n".join(format_order_record(o) for o in filtered[:5])
            return [f"{summary}\n\n{top_formatted}"]

        return ["No matching records found."]
