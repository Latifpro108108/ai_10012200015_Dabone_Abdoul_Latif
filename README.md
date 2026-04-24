# 🇬🇭 Ghana Intelligence RAG Chatbot
**Academic City University College | CS4241 - Introduction to AI**

**Student:** Dabone Abdoul Latif  
**Index Number:** 10012200015  
**Lecturer:** Godwin N. Danso  

---

## 🌟 Project Overview
This project is a high-integrity **Retrieval-Augmented Generation (RAG)** system designed to provide accurate, grounded answers regarding the **2025 Ghana Budget Statement** and the **2020 Regional Election Results**. 

The system moves beyond standard RAG by implementing **Evidence Triangulation**, ensuring that sensitive governmental and political data is cross-verified across multiple retrieval methodologies before a response is generated.

---

## 🏗️ Project Architecture (The "Parts" Framework)
The project is structured into logical components, each documented with its own summary and dedicated Git branch for transparency:

- **Part A: Data Preparation** — PDF/CSV ingestion, recursive character chunking, and metadata enrichment.
- **Part B: Custom Retrieval** — Hybrid Search implementation combining FAISS (Vector) and BM25 (Keyword).
- **Part C: Prompt Engineering** — Iterative template design with strict hallucination controls.
- **Part D: Full RAG Pipeline** — End-to-end integration with staged logging for every query.
- **Part E: Adversarial Testing** — Critical evaluation using ambiguous and misleading queries to prove robustness.
- **Part F: System Design** — Technical architecture breakdown and domain-specific justification.
- **Part G: Innovation** — The **Evidence Triangulation Engine** with automated confidence scoring.

---

## 🔬 Core Innovation: Evidence Triangulation (Part G)
To ensure zero-hallucination in the "Government & Election" domain, this system implements a novel **Triple-Path Retrieval** strategy:

### 1. The Three Independent Paths:
1.  **Path 1 (Semantic)**: Uses FAISS Vector search to find conceptual meaning.
2.  **Path 2 (Keyword)**: Uses BM25 to find exact financial figures and names.
3.  **Path 3 (Domain-Gated)**: A "Smart Filter" that identifies if a query is about *Elections* or *Budgets* and blocks irrelevant data sources.

### 2. Automated Confidence Scoring
An **Arbiter LLM** compares all three outputs to assign a **Confidence Level**:
- **✅ HIGH**: All retrieval paths agree (factually certain).
- **⚠️ MEDIUM**: Paths disagree, but a majority consensus is found.
- **❌ LOW**: All paths provide different or missing info (unreliable).

**Case Study Success**: When asked for GDP growth, the Semantic path initially misinterpreted a section (3.1%), but the Keyword/Domain paths correctly identified 5.7%. The system flagged this as **MEDIUM CONFIDENCE** and provided the correct 5.7% figure.

---

## 📊 Detailed Project Results

### 📁 Part A: Data Preparation Results
We processed two primary datasets with specific cleaning strategies:
- **Election CSV**: Cleaned non-breaking spaces (`\xa0`), removed `%` signs, and converted votes to integers. (615 valid rows).
- **Budget PDF**: Removed repeated headers/footers, skipped blank pages, and handled Windows encoding errors. (~91,000 words).
- **Chunking Strategy**: 
    - **PDF**: Large chunks (300 words, 50 overlap) to preserve context.
    - **CSV**: 1 row = 1 chunk to keep facts atomic.

### 🔍 Part B: Retrieval & The "NDC/NDP" Fix
We identified a critical failure in standard Vector Search:
- **The Failure**: Pure vector search treats `NDC` and `NDP` as identical because their embeddings are too similar.
- **The Fix**: **Hybrid Search (FAISS + BM25)**. BM25 performs an exact string match for "NDC", ensuring the correct party is always retrieved.
- **Result**: Accuracy improved from ~60% (guessing parties) to **100%** on keyword-specific queries.

### ✍️ Part C: Prompt Engineering Experiments
Tested two prompt versions to control AI behavior:
- **v1 (Strict/Structured)**: "The NDC vote percentage in Volta was 84.83%." (Better for research).
- **v2 (Concise)**: "84.83%." (Better for data extraction).
- **Verdict**: Both successfully avoided hallucinations by using a "Strict I do not know" clause.

### 🛡️ Part D & E: Adversarial Testing Results
The system was tested against "trick" queries to evaluate robustness:

| Metric | Pure LLM (No RAG) | Ghana Intelligence (RAG) |
|---|---|---|
| **Accuracy** | ❌ Failed (Guesses 2024 winners) | ✅ **Superior** (Cites 2020 sources) |
| **Hallucination** | Low (Admitted ignorance) | **ZERO** (Strictly refuses to invent data) |
| **Consistency** | Variable | **High** (Tethered to the index) |

---

## 🛠️ System Architecture (Part F)
- **Retrieval**: FAISS (High-speed vector) + BM25 (Keyword accuracy).
- **Embedding Model**: `all-MiniLM-L6-v2` (Fast & CPU-friendly).
- **LLM Engine**: **Llama-3.3-70B via Groq** (70B intelligence at millisecond speeds).
- **UI**: Streamlit (Professional Workstation with Pipeline Inspector).

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repo and install dependencies
pip install -r requirements.txt

# Setup environment variables
echo "GROQ_API_KEY=your_key_here" > .env
```

### 2. Launching the App
```bash
streamlit run app.py
```

---
© 2026 Dabone Abdoul Latif | Academic City University College
