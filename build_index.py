# app/build_index.py

import pickle
import faiss

# ✅ Load chunks, index, and model from chunks.pkl
with open("chunks.pkl", "rb") as f:
    chunk_list, index, model = pickle.load(f)

# Optionally save index separately if needed
faiss.write_index(index, "faiss.index")

# Optionally save chunks or model separately if needed
with open("sources.pkl", "wb") as f:
    pickle.dump(["source.txt"] * len(chunk_list), f)  # placeholder if source tracking needed

print("✅ FAISS index loaded from chunks.pkl and saved as faiss.index")
