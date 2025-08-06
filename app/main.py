from fastapi import FastAPI
from app.models import QueryInput
from app.document_parser import extract_text_from_file
from app.chunker import chunk_text
from app.embedder import embed_chunks
from app.retriever import search_top_chunks
from app.responder import get_answer, QueryRequest
from app.chunk_retriever import index, model, chunk_list  # make sure these are not conflicting

import faiss

app = FastAPI()


def get_best_answer(sources, query):
    keywords = ["pre-existing", "waiting period", "preexisting", "disease", "illness"]
    query_lower = query.lower()

    for s in sources:
        text_lower = s['text'].lower()
        if any(keyword in text_lower for keyword in keywords):
            return s['text']

    return sources[0]['text'] if sources else "No relevant information found."


@app.post("/query")
def query(request: QueryRequest):
    print("🧪 DEBUG | chunk_list type:", type(chunk_list), "len:", len(chunk_list))
    print("🧪 DEBUG | chunk_list[0]['text']:", chunk_list[0]['text'][:100] if isinstance(chunk_list, list) else "Not a list")


    top_chunks = search_top_chunks(request.query, index, chunk_list, model)
    answer = get_best_answer(top_chunks, request.query)

    return {
        "question": request.query,
        "answer": answer,
        "sources": top_chunks,
        "logic": "Answer selected using keyword filtering over retrieved chunks"
    }


@app.post("/api/v1/hackrx/run")
def run_query(data: QueryInput):
    try:
        text = extract_text_from_file(data.documents)
        print("✅ Step 1: PDF Extracted")
        if not text.strip():
            return {"error": "No text extracted from the document."}

        chunks = chunk_text(text)
        print("✅ Step 2: Chunks Created")

        # Avoid variable conflict here
        temp_index, temp_embeddings, temp_chunk_list, temp_model = embed_chunks(chunks)
        print("✅ Step 3: Embeddings Created")

        all_answers = []
        for question in data.questions:
            top_chunks = search_top_chunks(question, temp_index, temp_chunk_list, temp_model)
            print(f"✅ Step 4: Retrieved Chunks for question: {question}")
            answer = get_answer(question, top_chunks)
            print(f"✅ Step 5: Answer Generated")

            logic = f"Top {len(top_chunks)} semantically similar chunks selected based on cosine similarity."

            all_answers.append({
                "question": question,
                "answer": answer["answer"] if isinstance(answer, dict) else answer,
                "sources": top_chunks,
                "logic": logic
            })

        return {"results": all_answers}

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return {"error": str(e)}


# Debug: Confirm data types at startup
print("🟢 Startup Debug — Type of index:", type(index))
print("🟢 Startup Debug — Type of chunk_list:", type(chunk_list))
