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
- **Why this model?** It is small, fast, and works perfectly on a normal computer CPU without needing an expensive graphics card (GPU).

---

## Step 2 – Vector Storage (Task 2)

We used **FAISS** (Facebook AI Similarity Search) to store our embeddings.
- Instead of searching through the text one by one, FAISS allows us to search thousands of chunks in milliseconds by measuring the "distance" between the question vector and the chunk vectors.
- We saved the index to `indexes/rag_index.faiss` so we don't have to re-calculate it every time.

---

## Step 3 – Retrieval (Task 3)

We built a `search()` function that:
1. Takes the user's question.
2. Converts it into a vector.
3. Finds the **Top 5** chunks that are mathematically closest to that question.

---

## Step 4 – Hybrid Search (Advanced Feature - Task 4)

We implemented **Hybrid Search**, which is the "Gold Standard" for modern RAG systems.
- **Vector Search** is great for *meaning* (synonyms).
- **BM25 (Keyword Search)** is great for *specific words* (like "2025" or "inflation").
- By combining them, we get the best of both worlds.

---

## Step 5 – Failure Case & Fix (Task 5)

### The Failure
- **Query:** "What is the targeted inflation rate for 2025?"
- **The Problem:** Vector search alone sometimes gets confused by other paragraphs that talk about "2025" and "economics" but don't contain the specific word "inflation." It might return a general policy summary instead of the specific fact.

### The Fix
- **The Solution:** By using **Hybrid Search**, the word "inflation" acts as a strong signal. Even if the vector distance is slightly higher, the BM25 score for the word "inflation" pulls the correct chunk to the top.

---

## Output

At the end of Part B, we have:
- `indexes/rag_index.faiss` — The searchable vector database.
- A robust `hybrid_search()` function ready to be used in our app.
