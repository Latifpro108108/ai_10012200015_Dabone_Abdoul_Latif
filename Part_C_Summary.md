# Part C Summary: Prompt Engineering

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015

### 1. Prompt Design
I created two main prompt versions to test how instructions affect the output:
- **v1**: Focuses on preventing hallucinations by instructing the model to say "I don't know" if the context is missing.
- **v2**: Focuses on direct and concise answers based strictly on the provided documents.

### 2. Context Management
To prevent exceeding the model's token limit, I implemented a truncation strategy:
- Limited retrieval to the top 3 most relevant chunks.
- Set a hard character limit (4000 characters) for the injected context.
- This ensures the model always has enough space to generate a response without cutting off.

### 3. Results
Running experiments with the same query across both prompts showed:
- **v1** was more cautious and better at staying within the provided text.
- **v2** provided shorter, more readable responses suitable for a chatbot.

These prompts will be integrated into the final application in Part D.
