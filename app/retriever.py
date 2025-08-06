# import numpy as np

# # def search_top_chunks(question, index, chunks, model, top_k=3):
# #     query_vec = model.encode([question])
# #     D, I = index.search(np.array(query_vec), top_k)
# #     return [chunks[i] for i in I[0]]

# def search_top_chunks(question, index, chunk_list, model, top_k=5):
#     question_embedding = model.encode(question)
#     D, I = index.search(np.array([question_embedding]), top_k)

#     top_chunks = []
#     for i, score in zip(I[0], D[0]):
#         if i < len(chunk_list):
#             top_chunks.append({
#                 "text": chunk_list[i][:300],  # truncate to 300 chars
#                 "score": float(score)
#             })

#     return top_chunks

# app/retriever.py
import numpy as np

# Add domain-relevant keywords here
IMPORTANT_KEYWORDS = [
    "pre-existing", "maternity", "waiting period", "exclusion",
    "hospitalization", "dental", "critical illness", "accident", "coverage",
    "premium", "claim", "cashless", "network hospital"
]

def search_top_chunks(question, index, chunk_list, model, top_k=10):
    # Step 1: Embed the query
    question_embedding = model.encode(question)
    if isinstance(question_embedding, list):
        question_embedding = np.array(question_embedding)

    if question_embedding.ndim == 1:
        question_embedding = question_embedding.reshape(1, -1)

    # Step 2: Semantic search via FAISS
    D, I = index.search(question_embedding, top_k)

    # Step 3: Collect retrieved chunks
    top_chunks = []
    for i, score in zip(I[0], D[0]):
        if i < len(chunk_list):
            text = chunk_list[i]["text"][:300]   # Optional truncate for display
            top_chunks.append({
                "text": text,
                "score": float(score)
            })

    # Step 4: Filter chunks with keyword presence
    keyword_hits = [
        chunk for chunk in top_chunks
        if any(keyword['text'].lower() in chunk['text'].lower() for keyword in top_chunks)
    ]

    # Step 5: Return keyword hits if any, else fallback to original top_chunks
    return keyword_hits if keyword_hits else top_chunks
