# Part D Summary: Full RAG Pipeline Implementation

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## 1. Objective
The goal of Part D was to integrate the modular components from Parts A, B, and C into a single, automated **RAG Pipeline**. This ensures that the Retrieval (Part B) and the Prompt Engineering (Part C) work together seamlessly to provide accurate, grounded answers.

---

## 2. Integration Proof (How the parts connect)
The pipeline demonstrates full integration through the following markers:
- **Retrieval Connection**: The pipeline uses the `hybrid_search` logic and FAISS index from Part B to find the top chunks.
- **Context Connection**: The selected chunks are passed directly into the prompt templates designed in Part C.
- **Traceability**: Every answer includes the **Similarity Scores** and **Source Metadata**, proving that the LLM is not "hallucinating" but is reading the specific files processed in Part A.

---

## 3. Real-World Pipeline Test
We tested the pipeline with the query: **"What is your say about the inflation?"**

### Stage 1: Retrieval Results
The system successfully retrieved 3 relevant chunks from the budget document:
- **Chunk 1 (Score: 0.6874)**: Focuses on the CPI rebasing and previous inflation efforts.
- **Chunk 2 (Score: 0.5391)**: Focuses on global economic growth and inflation trends (5.8% in 2024).
- **Chunk 3 (Score: 0.5333)**: Focuses on Ghana's 2024 inflation ending at 23.8%.

### Stage 4: LLM Response
The model used the retrieved context to provide a grounded summary:
- **Global View**: World inflation declined to 5.8% in 2024.
- **Local View**: Ghana's inflation ended 2024 at 23.8%, exceeding the IMF and budget targets.

---

## 4. Pipeline Logging
I implemented a 4-stage logging system using `print()` statements:
1.  **[LOG] Stage 1 (Retrieval)**: Displays the query, the number of chunks found, and their scores.
2.  **[LOG] Stage 2 (Context)**: Confirms the building of the context block.
3.  **[LOG] Stage 3 (Prompt)**: Prints the **raw prompt** (with instructions + context) for verification.
4.  **[LOG] Stage 4 (Generation)**: Logs the request to the LLM and the completion of the process.

---

## Files in This Part
- **`part_d_pipeline.ipynb`**: The unified backend pipeline with stage-by-stage logging.
- **`Part_D_Summary.md`**: This summary report.
