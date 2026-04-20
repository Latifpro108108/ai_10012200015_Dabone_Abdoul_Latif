# System Architecture & Design Justification

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## 1. Architecture Breakdown

### A. Data Flow (The Journey of a Query)
1.  **Input**: The user submits a natural language query via the interface.
2.  **Pre-processing**: The query is normalized (lowercase, punctuation removed) to match the BM25 tokens.
3.  **Hybrid Retrieval**: 
    *   **Semantic Path**: The query is converted into a vector embedding using `all-MiniLM-L6-v2` and compared against the FAISS index to find "meaning-based" matches.
    *   **Keyword Path**: The query is tokenized and searched against the BM25 index to find "exact-word" matches (critical for financial figures).
4.  **Fusion**: Scores from both paths are normalized and combined. The Top 3 most relevant chunks are selected.
5.  **Prompting**: The selected chunks are injected into a "Strict Instruction" prompt template.
6.  **Inference**: The grounded prompt is sent to the Llama-3.3-70B model via Groq for high-speed response generation.

### B. Component Interaction
-   **Storage Layer**: Uses JSON for raw text storage and FAISS for efficient high-dimensional vector search.
-   **Logic Layer**: Python orchestrates the "Retrieval-Selection-Prompting" loop.
-   **Inference Layer**: Groq Cloud provides the computational power to run a 70-billion parameter model in milliseconds, ensuring a smooth user experience.

---

## 2. Design Justification

### Why this design is suitable for the domain (Government & Elections):

1.  **Figure Accuracy (Hybrid Search)**: 
    *   In government budgets, a single number (e.g., "5.8% inflation") is more important than the general "vibe" of the text. 
    *   **Justification**: Standard RAG often misses specific numbers. By adding **BM25 Keyword Search**, we ensure that if a user asks for a specific figure, the system finds the exact table row containing that number.

2.  **Zero Hallucination (Strict Prompting)**: 
    *   Election results are sensitive. Guessing a winner is unacceptable.
    *   **Justification**: Our architecture uses a "Strict Context" prompt that forces the LLM to say "I don't know" if the data is missing. This makes the system reliable for academic and official use.

3.  **Modular Scalability**:
    *   Government data changes every year.
    *   **Justification**: This architecture is "plug-and-play." We can add the 2026 budget simply by chunking it and adding it to the FAISS index without ever needing to retrain or fine-tune the AI model.

4.  **Performance (Groq Integration)**:
    *   Users expect instant answers.
    *   **Justification**: By using Groq's LPU (Language Processing Unit) architecture, we deliver 70B-level intelligence at the speed of a smaller model, making the RAG pipeline feel instantaneous.
