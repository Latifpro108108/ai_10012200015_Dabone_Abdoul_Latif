# Part D Summary: Full Pipeline & Critical Evaluation

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## 1. Pipeline Implementation
I built a unified `rag_pipeline(query)` function that connects Retrieval, Context Selection, and Prompting into a single automated flow. As required, the function includes **logging at each stage** to provide transparency.

---

## 2. Adversarial Testing & Comparison
To evaluate the system's reliability, I compared the **RAG System** against a **Pure LLM** (no retrieval) using adversarial queries designed to trigger hallucinations.

### Test Case: *"How many votes did the NPP get in the 2025 budget?"*
- **Pure LLM**: Tries to answer based on general knowledge and often mixes election years or confuses the "2025 budget" context with an "election" context.
- **RAG System**: Correctly identifies that the context provided (the 2025 Budget) does not contain election vote counts. It refuses to hallucinate and correctly states the information is missing.

### Comparative Metrics

| Metric | Pure LLM | RAG System |
|---|---|---|
| **Accuracy** | Low (General knowledge) | High (Context-driven) |
| **Hallucination** | High (Guesses facts) | Very Low (Restricted) |
| **Groundedness** | Not Grounded | Fully Grounded |

---

## 3. Final Observations
- The **Retrieval Stage** (Stage 1) successfully filters out irrelevant data.
- The **Context Selection** (Stage 2) ensures only the most high-scoring chunks are used.
- The **Logging System** provides evidence of exactly what data the LLM is reading before it answers.

This integrated approach ensures the chatbot is a reliable tool for analyzing official Ghana government documents.
