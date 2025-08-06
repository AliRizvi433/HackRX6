# app/chunk_retriever.py

import faiss
import pickle
from sentence_transformers import SentenceTransformer
import numpy as np

# Correctly unpack from the pickle file
with open("chunks.pkl", "rb") as f:
    data = pickle.load(f)

    # Either unpack directly if it's a 3-tuple
    if isinstance(data, tuple) and len(data) == 3:
        chunk_list = data[0]  # or 1, depending on your saving order
    else:
        chunk_list = data  # fallback: assume it's already a list

# Load FAISS index
index = faiss.read_index("faiss.index")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")


def query_index(query: str, top_k: int = 5):
    """
    Search the FAISS index for the top_k most relevant chunks for the given query.
    """
    query_embedding = model.encode([query])
    scores, indices = index.search(query_embedding.astype("float32"), top_k)

    results = []
    for i, l2_distance in zip(indices[0], scores[0]):
        if i == -1 or i >= len(chunk_list):
            continue

        # Convert L2 distance to similarity score (higher is better)
        similarity = 1 / (1 + l2_distance)

        # Filter out bad matches (very small similarity)
        if not np.isfinite(similarity) or similarity < 0.01:
            continue

        chunk = chunk_list[i]
        results.append({
            "text": chunk.get('text', ''),
            "clause_type": chunk.get('clause_type', 'Unknown'),
            "score": round(float(similarity), 4)  # rounded for readability
        })


    return results


# Make the variables accessible to importers
__all__ = ["chunk_list", "index", "model", "query_index"]
