# Part B Summary – Custom Retrieval System
**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence  
**Lecturer:** Godwin N. Danso  

---

## What We Did

In Part B, we built the "brain" of the chatbot—the part that understands questions and finds the right information from the thousands of words we processed in Part A.

---

## Step 1 – The Embedding Pipeline (Task 1)

We used the **sentence-transformers** library with the **all-MiniLM-L6-v2** model. 
- **What is an embedding?** It is a list of 384 numbers that represents the *meaning* of a piece of text. 
- **Why this model?** It is small, fast, and works perfectly on a normal computer CPU.

---

## Step 2 – Vector Storage (Task 2)

We used **FAISS** (Facebook AI Similarity Search) to store our embeddings.
- Instead of searching text one by one, FAISS searches thousands of chunks in milliseconds using vector distance.
- The index is saved to `indexes/rag_index.faiss`.

---

## Step 3 – Retrieval (Task 3)

We built a search function that converts questions into vectors and retrieves the **Top 5** closest chunks.

---

## Step 4 – Hybrid Search (Task 4)

We implemented **Hybrid Search**:
- **Vector Search** for semantic meaning.
- **BM25** for exact keyword matching (e.g., "2025", "inflation").
- This combination ensures higher accuracy than using either method alone.

---

## Step 5 – Verification & Accuracy (Task 5)

We verified the system by running test queries to ensure the most relevant data is returned.

**Example Test Case:**
- **Query:** "How many votes did Nana Addo get in the Ahafo region?"
- **Top Result:** "In the 2020 Ghana election, Nana Akufo Addo from NPP got 145,584 votes (55.04%) in Ahafo Region."
- **Accuracy Check:** The system successfully matched "Nana Addo" with "Nana Akufo Addo" and prioritized the specific election result chunk with a high similarity score (0.85+).

---

---

## Step 6 – Critical Task: Failure Case & Fix

We identified and **verified** a real failure case where pure vector search returns wrong results, and demonstrated the fix.

### The Failure
- **Query:** `"What were the NDC votes in Savannah in 2020?"`
- **Root Cause:** The `all-MiniLM-L6-v2` embedding model encodes short political acronyms `NDC` (National Democratic Congress) and `NDP` (National Democratic Party) into nearly **identical vector representations**, because they are short, rare tokens with no rich contextual signal.
- **Result:** Pure vector search returns **NDP (Nana Konadu Agyeman Rawlings)** results — a completely **different party** — instead of the correct NDC results.

### The Fix: Hybrid Search
By combining **BM25 keyword matching** with vector search:
- **BM25** performs an exact string match for the token `NDC`, cleanly distinguishing it from `NDP`.
- **Vector Search** still contributes semantic context for words like *votes*, *Savannah*, and *2020*.

| | Pure Vector Search | Hybrid Search (Fix) |
|---|---|---|
| NDC vs NDP | ❌ Treated as nearly identical | ✅ Exact keyword match via BM25 |
| Top Result | ❌ NDP (Wrong party) | ✅ NDC/Mahama — 144,244 votes in Savannah |

### Conclusion
This demonstrates why a hybrid retrieval system is more robust than pure semantic search, especially in domains with domain-specific acronyms and terminology.

---

## Output

- `indexes/rag_index.faiss` — The searchable vector database.
- A robust `hybrid_search()` function ready for the final application.
- Verified failure/fix demonstration in the retrieval notebook (Cells 3–5).
