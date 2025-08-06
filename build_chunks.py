import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.chunker import chunk_text
from app.document_parser import extract_text_from_file  # ✅ new unified extractor

# Step 1: Load and parse all supported files
folder_path = "data"
all_text = ""

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    try:
        text = extract_text_from_file(file_path)
        if text.strip():  # skip empty
            all_text += text + "\n"
            print(f"✅ Processed: {filename}")
        else:
            print(f"⚠️ Empty or unreadable: {filename}")
    except Exception as e:
        print(f"❌ Failed to process {filename}: {e}")

# Step 2: Chunk the text
raw_chunks = chunk_text(all_text, chunk_size=300, overlap=50)
chunk_list = [{"text": chunk} for chunk in raw_chunks]


# Step 3: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 4: Generate embeddings
embeddings = model.encode([chunk["text"] for chunk in chunk_list])


# Step 5: Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Step 6: Save to pickle
with open("chunks.pkl", "wb") as f:
    pickle.dump((chunk_list, index, model), f)

print("✅ chunks.pkl created with", len(chunk_list), "chunks.")
