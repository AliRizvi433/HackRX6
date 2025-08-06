# app/test_retriever.py

from retriever import retrieve_top_k_chunks

query = "Is maternity leave covered in this policy?"
top_k = 3

results = retrieve_top_k_chunks(query, k=top_k)

print(f"\nTop {top_k} retrieved chunks for query: '{query}'\n")
for i, chunk in enumerate(results, 1):
    print(f"--- Chunk {i} ---")
    print(chunk)
    print()
