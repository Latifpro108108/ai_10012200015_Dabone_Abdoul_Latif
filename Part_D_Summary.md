# Part D & E Summary: Pipeline & Critical Evaluation

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## 🟢 PART D: PIPELINE IMPLEMENTATION

### 1. Objective
To connect the modular components (Retrieval, Context, Prompt) into a single automated flow with **staged logging** for transparency.

### 2. Execution Log Evidence
The `rag_pipeline(query)` function logs every stage:
- **Stage 1 (Retrieval)**: Displays chunks found and their hybrid scores.
- **Stage 2 (Context)**: Displays source metadata and text aggregation.
- **Stage 3 (Prompt)**: Prints the character-for-character prompt sent to the LLM.
- **Stage 4 (LLM)**: Displays the final grounded response.

---

## 🔴 PART E: CRITICAL EVALUATION & ADVERSARIAL TESTING

### 1. Adversarial Testing Strategy
I used a misleading query to test if the system could be tricked into mixing election results with budget data:
- **Query:** *"How many votes did the NPP get in the 2025 budget?"*

### 2. RAG System vs. Pure LLM Comparison

| Metric | Pure LLM (No Retrieval) | RAG System (Grounded) |
|---|---|---|
| **Accuracy** | Low (Guesses facts) | High (Data-driven) |
| **Hallucination** | High risk | Zero (Refuses to answer if not in context) |
| **Evidence** | None | Cites Source: Budget |

### 3. Key Finding
When asked about "votes in the 2025 budget," the **Pure LLM** tried to guess, but the **RAG System** correctly responded **"I don't know."** This proves that the pipeline successfully prevents hallucinations by sticking strictly to the provided documents.

---

## Final Deliverables
- **`part_d_pipeline.ipynb`**: Contains both Part D and Part E implementations.
- **`Part_D_Summary.md`**: Consolidated report for both parts.
