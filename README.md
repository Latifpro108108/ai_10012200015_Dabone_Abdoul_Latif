# 🇬🇭 Ghana Intelligence RAG Chatbot
**Academic City University College | CS4241 - Introduction to AI**

**Student:** Dabone Abdoul Latif  
**Index Number:** 10012200015  
**Lecturer:** Godwin N. Danso  

---

## 🌟 Project Overview
This project is a high-integrity Retrieval-Augmented Generation (RAG) system designed to provide accurate, grounded answers regarding the **2025 Ghana Budget Statement** and the **2020 Regional Election Results**. 

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

## 🔬 Core Innovation: Evidence Triangulation
To ensure zero-hallucination in the "Government & Election" domain, this system implements a novel **Triple-Path Retrieval** strategy:
1.  **Path 1 (Semantic)**: Captures conceptual meaning via FAISS.
2.  **Path 3 (Keyword)**: Ensures exact figure accuracy via BM25.
3.  **Path 3 (Domain-Gated)**: Automatically filters sources (Budget vs. Election) to prevent data contamination.

An **Arbiter LLM** compares all three outputs to assign a **Confidence Level (High/Medium/Low)**, allowing the system to flag unreliable answers rather than guessing.

---

## 🖥️ Applications & Interfaces
This solution provides two distinct interfaces to cater to different user needs:

This solution provides the following interface:

1.  **Ghana Intelligence Workstation (`app.py`)**: A professional research tool featuring a **RAG Pipeline Inspector**. It allows users to toggle "Innovation Mode" and view the raw retrieval chunks, similarity scores, and the final prompt sent to the LLM.

---

## 🌿 Git Branching Strategy
This repository follows a structured branching model. Each branch corresponds to a specific phase of the project and contains its own detailed implementation notes:
- `part-a`, `part-b`, `part-c`, `part-d-e`: Incremental development stages.
- `main`: The stable core codebase.
- `final-deliverable`: The polished, submission-ready version of the full system.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.10+
- Groq API Key

### 2. Installation
```bash
# Clone the repo and install Python dependencies
pip install -r requirements.txt

# Setup environment variables
echo "GROQ_API_KEY=your_key_here" > .env
```

### 3. Launching the App
```bash
streamlit run app.py
```

---
© 2026 Dabone Abdoul Latif | Academic City University College
