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
1. **Environment Setup**:
   Create a `.env` file and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_key_here
   ```
2. **Install Dependencies**:
   ```bash
   pip install streamlit groq sentence-transformers faiss-cpu rank-bm25 python-dotenv pandas pymupdf
   ```
3. **Run the Application**:
   ```bash
   streamlit run app.py
   ```

## Project Structure
- `part_a_data_prep.ipynb`: Data cleaning and chunking logic.
- `part_b_retrieval.ipynb`: Indexing and hybrid search implementation.
- `part_c_prompt_engineering.ipynb`: Prompt template design.
- `Part_D_and_E_Pipeline_and_Evaluation.ipynb`: Consolidated backend and evaluation.
- `app.py`: Final Streamlit User Interface.

---
© 2026 Dabone Abdoul Latif | Academic City University College
