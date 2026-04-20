# PART G: INNOVATION COMPONENT — EVIDENCE TRIANGULATION

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## 1. The Innovation: Evidence Triangulation Engine
For the innovation component, I developed a **Domain-Specific Evidence Triangulation Engine**. Unlike standard RAG systems that rely on a single retrieval pass, this system cross-references evidence from three independent "points of view" before answering.

### The Three Independent Paths:
1.  **Path 1 (Semantic)**: Uses FAISS Vector search to find conceptual meaning.
2.  **Path 2 (Keyword)**: Uses BM25 to find exact financial figures and names.
3.  **Path 3 (Domain-Gated)**: A "Smart Filter" that automatically identifies if a query is about *Elections* or *Budgets* and blocks irrelevant data sources to prevent contamination.

## 2. Novel Feature: Automated Confidence Scoring
The core innovation is an **Arbiter LLM Step**. It compares the answers from all three paths and assigns a Confidence Level:
- **✅ HIGH**: All retrieval paths agree (factually certain).
- **⚠️ MEDIUM**: Paths disagree, but a majority consensus is found.
- **❌ LOW**: All paths provide different or missing info (unreliable).

## 3. Evidence of Success (Results Analysis)

### Case Study: "What was Ghana's GDP growth rate in 2024?"
- **Standard RAG Problem**: In tests, the Semantic path (Path 1) returned an incorrect figure of 3.1% by misinterpreting a different section of the text.
- **Innovation Solution**: The Keyword and Domain paths correctly identified 5.7%. The system detected this discrepancy, assigned **MEDIUM CONFIDENCE**, and correctly chose 5.7% as the Best Answer.
- **Impact**: This prevents the AI from confidently stating incorrect financial figures.

### Case Study: Domain Isolation
- **Test**: When asked about the "Total government expenditure in 2024", the system's **Domain Gate** successfully blocked 100% of the election data, ensuring the answer was strictly grounded in the Budget Statement.

## 4. Why this is Suitable for the Domain
In the context of **Ghanaian Government and Election data**, accuracy is paramount. This innovation moves the AI from "guessing" to "verifying," making it a professional-grade tool for researchers and citizens who require high-integrity data. It ensures that sensitive political or economic information is double-checked against multiple search methodologies before being presented to the user.
