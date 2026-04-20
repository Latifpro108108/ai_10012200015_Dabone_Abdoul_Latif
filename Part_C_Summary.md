# Part C Summary: Prompt Engineering

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015

### 1. Prompt Design
I designed two prompt versions to test how strict instructions affect the AI's reliability:
- **v1**: Includes a strict "I do not know" clause to prevent hallucinations.
- **v2**: A direct instruction to be concise and stick only to the provided documents.

### 2. Context Management
To ensure the system works within the LLM's token limits, I used the following strategy:
- **Integration**: The system loads the `rag_index.faiss` and the embedding model directly from Part B.
- **Ranking**: It uses the Hybrid Search logic to pick the top 3 most relevant chunks.
- **Truncation**: The combined text is limited to 4000 characters to prevent prompt overflow.

### 3. Experimental Results
I tested the system with the query: *"What is the inflation target for 2025?"*

**Observations:**
- The **Retrieval System (Part B)** correctly identified chunks discussing 2025 economic outlooks and 2024 inflation targets.
- The **LLM (Part C)** correctly identified that while 2024 targets and 2025 *projections* exist in the text, the specific *target* for 2025 was not explicitly stated.
- Both prompts successfully prevented the AI from making up a number, with **v1** giving a very clear "I do not know" response as instructed.

This proves that the connection between the Retrieval (Part B) and the Prompt (Part C) is working perfectly to provide honest, data-driven answers.
