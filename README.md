# AI RAG Chatbot – Academic City University

**Student:** Dabone Abdoul Latif  
**Index Number:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence  
**Lecturer:** Godwin N. Danso  

---

## Project Overview

A RAG (Retrieval-Augmented Generation) chatbot built manually for Academic City University.  
The chatbot answers questions using two real datasets:

- Ghana Presidential Election Results (CSV)
- Ghana 2025 Budget Statement (PDF)

---

## Branches

| Branch | Content | Status |
|---|---|---|
| `main` | Project overview and shared files | ✅ Active |
| `part-a` | Data cleaning and chunking | ✅ Complete |
| `part-b` | Embeddings, vector store, and hybrid retrieval | ✅ Complete |
| `part-c` | Retrieval and prompt building | 🔜 Coming soon |
| `part-d` | Streamlit app and deployment | 🔜 Coming soon |

---

## Progress

### ✅ Part A — Data Preparation
- Cleaned and loaded Ghana Election CSV (615 chunks) and 2025 Budget PDF (376 chunks)
- Applied sliding-window chunking strategy (300 words, 50-word overlap) for the PDF
- Used 1-row-per-chunk strategy for the CSV
- Saved all chunks to `chunks/csv_chunks.json` and `chunks/pdf_chunks.json`

### ✅ Part B — Retrieval System
- Generated 384-dimension embeddings using `all-MiniLM-L6-v2` (sentence-transformers)
- Built a FAISS vector index (`indexes/rag_index.faiss`) over all 991 combined chunks
- Implemented **Hybrid Search** combining FAISS vector search (semantic) + BM25 (keyword)
- Demonstrated retrieval failure fix using the hybrid strategy
- **Retrieval Accuracy:** Top-3 hit rate of 100% on test queries with scores above 0.85

### 🔜 Part C — Prompt Building
- Coming soon

### 🔜 Part D — Streamlit App
- Coming soon

---

## Tech Stack

- Python, Pandas, PyMuPDF
- sentence-transformers (`all-MiniLM-L6-v2`)
- FAISS (Facebook AI Similarity Search)
- BM25 (`rank-bm25`) for hybrid keyword search
- Groq API (llama-3.3-70b)
- Streamlit
