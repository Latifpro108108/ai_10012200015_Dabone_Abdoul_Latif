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
I tested the system with the query: *"What was the NDC vote percentage in the Volta region in 2020?"*

**Observations:**
- **Prompt v1 (Strict/Structured)**: Produced a full, explanatory sentence: *"The NDC vote percentage in the Volta region in 2020 was 84.83%."* This is better for a conversational experience.
- **Prompt v2 (Concise)**: Produced the ultra-short answer: *"84.83%"*. This is better for data extraction or minimal interfaces.
- **Accuracy**: Both prompts correctly identified the data from the retrieved chunks (84.83%) and avoided any hallucination or outside knowledge.

**Evidence of Improvement:**
By iterating from v1 to v2, I demonstrated that I can control the **verbosity** and **precision** of the output simply by adjusting the instruction block, without needing to change the underlying retrieval logic.
