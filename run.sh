#!/bin/bash
#!/bin/bash
python3 build_chunks.py
python3 build_index.py
echo "Chunks rebuilt and FAISS index updated."

export OPENAI_API_KEY="your-key-here"
uvicorn app.main:app --host=0.0.0.0 --port=8000
