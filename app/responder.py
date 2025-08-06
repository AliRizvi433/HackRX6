from openai import OpenAI
from app.config import OPENAI_API_KEY
import re
from pydantic import BaseModel

client = OpenAI(api_key=OPENAI_API_KEY)

class QueryRequest(BaseModel):
    query: str

def get_answer(query: str, top_chunks: list[dict]) -> dict:
    # Step 1: Remove chunks with invalid scores
    valid_chunks = [
        chunk for chunk in top_chunks
        if isinstance(chunk["score"], (int, float)) and 0 < chunk["score"] < 1e6
    ]

    if not valid_chunks:
        return {
            "question": query,
            "answer": "Sorry, no valid chunks found in the index.",
            "sources": [],
            "logic": "All chunks had invalid or infinite scores."
        }

    # Step 2: Extract keywords from query
    query_keywords = set(re.findall(r'\w+', query.lower()))

    # Step 3: Keep only chunks that contain any keyword
    keyword_matched_chunks = [
        chunk for chunk in valid_chunks
        if any(kw in chunk["text"].lower() for kw in query_keywords)
    ]

    # Step 4: Fall back to valid_chunks if no keyword matches
    candidate_chunks = keyword_matched_chunks if keyword_matched_chunks else valid_chunks

    # Step 5: Sort by score (lower = better in FAISS)
    candidate_chunks.sort(key=lambda x: x["score"])
    best_chunk = candidate_chunks[0]

    # Step 6: Extract most relevant sentence from the best chunk
    answer = extract_relevant_text(query, best_chunk["text"])

    # Step 7: Fallback if answer is too vague or short
    if len(answer.strip()) < 15:
        answer = "The document does not explicitly mention the answer to this question."

    return {
        "question": query,
        "answer": answer,
        "sources": candidate_chunks[:3],
        "logic": f"Answer selected from keyword-matched chunks and score (top score: {best_chunk['score']:.2f})"
    }

def extract_relevant_text(question: str, context: str) -> str:
    question_keywords = set(re.findall(r'\w+', question.lower()))
    sentences = re.split(r'(?<=[.!?]) +', context)
    if not sentences:
        return context.strip()
    best_sentence = max(sentences, key=lambda s: len(question_keywords & set(s.lower().split())))
    return best_sentence.strip()
