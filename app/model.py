from sentence_transformers import SentenceTransformer

class MyEmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load embedding model '{model_name}': {e}")

    # app/model.py
from sentence_transformers import SentenceTransformer

class MyEmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        # Handles both single string or list of strings
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts)
