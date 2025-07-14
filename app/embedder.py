# app/embedder.py

from sentence_transformers import SentenceTransformer


class Embedder:
    """
    A wrapper around SentenceTransformer to generate embeddings
    for text chunks used in RAG pipelines.
    """

    def __init__(self, model_name="all-mpnet-base-v2"):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts):
        """
        Generate dense vector embeddings for a list of texts.
        """
        return self.model.encode(texts, convert_to_tensor=True)


# Optional helper functions
embedder_instance = Embedder()

def get_embeddings(texts):
    return embedder_instance.embed(texts)
