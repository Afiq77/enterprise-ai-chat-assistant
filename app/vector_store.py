# app/vector_store.py

import faiss
import numpy as np


class VectorStore:
    """
    In-memory vector store using FAISS for similarity search.
    Stores text chunks and enables semantic retrieval using dense embeddings.
    """

    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []
        self.dim = dim

    def add(self, embeddings, texts):
        """
        Add embeddings and corresponding text chunks to the store.
        """
        embeddings_np = np.array(embeddings, dtype=np.float32)
        self.index.add(embeddings_np)
        self.text_chunks.extend(texts)

    def search(self, query_embedding, top_k=3, chunks=None):
        """
        Perform similarity search on the text chunks using FAISS.

        If `chunks` are provided, search only over those; otherwise search entire store.
        """
        if chunks is None:
            chunks = self.text_chunks

        if not chunks:
            return ["⚠️ No matching chunks available for search."]

        # Map chunk text to FAISS index
        full_embeddings = self.index.reconstruct_n(0, self.index.ntotal)
        chunk_to_index = {text: i for i, text in enumerate(self.text_chunks)}

        # Filter based on given chunks
        filtered_indices = [chunk_to_index[c] for c in chunks if c in chunk_to_index]
        filtered_embeddings = [full_embeddings[i] for i in filtered_indices]

        if not filtered_embeddings:
            return ["⚠️ No matching embeddings found."]

        temp_index = faiss.IndexFlatL2(self.dim)
        temp_index.add(np.array(filtered_embeddings, dtype=np.float32))

        query_vec = np.array([query_embedding], dtype=np.float32)
        _, indices = temp_index.search(query_vec, top_k)
        return [chunks[i] for i in indices[0]]
