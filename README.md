🚀 LLM-Powered Query Retrieval System – HackRx 6.0
This project is an intelligent, explainable query–retrieval system built for HackRx 6.0. It enables users to upload insurance/legal/HR/compliance documents (PDF, DOCX, or email), ask natural language questions, and receive accurate answers grounded in document context, along with structured JSON output.

🧠 Features
📄 Multi-format Document Support: Accepts PDF, DOCX, and email data (EML)

🔍 Semantic Chunking: Documents are split into meaningful segments (clauses/sections)

🧬 Embeddings: Uses SentenceTransformer to encode document chunks for semantic search

⚡ FAISS Vector Search: Fast approximate nearest neighbor search for relevant clauses

🤖 LLM-Powered Responses: GPT-4 (or fallback) answers questions using retrieved context

📦 Structured JSON Output: Returns relevant clauses, source metadata, and final answer

🛠️ Installation
bash
Copy
Edit
git clone https://github.com/your-org/llm-query-retrieval.git
cd llm-query-retrieval
pip install -r requirements.txt
Ensure you have Python 3.9+ installed and a working OpenAI API Key.

▶️ Running the App Locally
bash
Copy
Edit
uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
For production use (no reload):

bash
Copy
Edit
uvicorn app.main:app --host=0.0.0.0 --port=8000
Make sure to export your OpenAI key:

bash
Copy
Edit
export OPENAI_API_KEY="your-key-here"
📤 Example API Request
http
Copy
Edit
POST /api/v1/hackrx/run
Authorization: Bearer <your_token>
Content-Type: application/json

{
  "documents": "<url_to_pdf_or_docx>",
  "questions": [
    "Does this policy cover knee surgery?",
    "What is the waiting period?"
  ]
}
✅ Sample Output
json
Copy
Edit
{
  "answers": [
    {
      "question": "Does this policy cover knee surgery?",
      "answer": "Yes, knee surgery is covered after a 3-month waiting period.",
      "source_clauses": [
        {
          "text": "Coverage includes orthopedic procedures such as knee surgery...",
          "clause_type": "Coverage",
          "score": 12.4
        }
      ]
    },
    ...
  ]
}
🧪 How it Works
Document Parsing:

Uses PDFMiner and python-docx to extract clean text

Chunking:

Splits text into logical paragraphs/clauses

Embedding:

Chunks are converted into vector embeddings using all-MiniLM-L6-v2

Indexing:

FAISS is used to store and search the chunks

Query Processing:

For each question, top relevant chunks are retrieved

LLM Response:

GPT-4 (or fallback) generates the final answer grounded in the retrieved context

Structured Output:

Answers are returned alongside metadata for explainability

🌐 Deployment (Replit Compatible)
Make sure your run.sh file includes:

bash
Copy
Edit
python build_chunks.py
python build_index.py
uvicorn app.main:app --host=0.0.0.0 --port=8000
You can deploy on Replit using the "Web Server" template. Paste your OpenAI key in .env.

📁 Directory Structure
arduino
Copy
Edit
.
├── app/
│   ├── main.py
│   ├── chunker.py
│   ├── chunk_retriever.py
│   ├── clause_classifier.py
│   ├── document_parser.py
│   ├── responder.py
│   └── ...
├── data/
├── build_chunks.py
├── build_index.py
├── chunks.pkl
├── faiss.index
├── run.sh
└── requirements.txt
🔒 Security Notes
All API calls require a Bearer token in Authorization header

Email and document URLs are sanitized before processing

📌 Submission Details
Webhook URL: https://<your-replit-url>.replit.app/api/v1/hackrx/run

Team Name: <Your Team>

Problem Statement: "Build an LLM-powered intelligent query retrieval system for enterprise docs"