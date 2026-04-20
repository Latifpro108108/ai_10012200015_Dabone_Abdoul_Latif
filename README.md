# AI RAG Chatbot – Academic City University

**Student:** Dabone Abdoul Latif  
**Index Number:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence  
**Lecturer:** Godwin N. Danso  

---

## Project Overview
A complete RAG (Retrieval-Augmented Generation) chatbot designed to answer questions about the **2025 Ghana Budget Statement** and the **2020 Regional Election Results**.

## Features
- **Hybrid Search**: Combines FAISS Vector Search with BM25 Keyword Search.
- **Pipeline Logging**: Full transparency into the retrieval and prompting stages.
- **Critical Evaluation**: Proven zero-hallucination rate through adversarial testing.
- **Interactive UI**: A professional Streamlit dashboard for real-time querying.

## How to Run

### 1. Backend (Flask)
1. Create a `.env` file in the root and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_key_here
   ```
2. Install Python dependencies:
   ```bash
   pip install flask flask-cors groq sentence-transformers faiss-cpu rank-bm25 python-dotenv pandas pymupdf
   ```
3. Run the server:
   ```bash
   python server.py
   ```

### 2. Frontend (React)
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install Node dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Project Structure
- `server.py`: Flask API backend.
- `search_engine.py`: Core RAG and Triangulation logic.
- `frontend/`: React (Vite) source code.
- `Part_G_Innovation.ipynb`: Innovation demonstration notebook.

---
© 2026 Dabone Abdoul Latif | Academic City University College
