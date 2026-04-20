# Part C – Prompt Engineering Summary

**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Introduction to Artificial Intelligence

---

## What This Part Is About

In Part C, we built the **prompt layer** — the bridge between the retrieved chunks (Part B) and the LLM (Groq).

A good prompt:
- Feeds the right context to the AI
- Tells the AI exactly how to behave
- Prevents hallucinations (made-up answers)
- Stays within the model's token limit

---

## Task 1 – Prompt Template Design

We designed **3 prompt templates**, each with a different communication style:

### Prompt A — Strict (Anti-Hallucination)
- Explicitly forbids the AI from using outside knowledge
- Forces the AI to say "I don't have that information" if the answer isn't in the context
- **Best for:** preventing made-up facts, high-stakes factual queries

### Prompt B — Loose (Friendly)
- Allows the AI to give more natural, flowing answers
- Less rigid instructions — the AI can interpret the context more freely
- **Best for:** general-purpose Q&A where readability matters more than precision

### Prompt C — Academic (Formal with Citations)
- Requires the AI to cite sources as [Source 1], [Source 2], etc.
- Uses formal, academic language
- **Best for:** project reports, academic submissions, verifiable answers

---

## Task 2 – Context Window Management

### The Problem
LLMs have a maximum token limit (Groq Llama: ~8,000 tokens).  
If we send too much text, the model cuts off or crashes.

### Our Token Budget
```
Total model limit:     8,000 tokens
System instructions:    ~200 tokens
User question:           ~30 tokens
Context (our limit):  1,000 tokens  ← controlled here
AI response reserved:   ~500 tokens
```

### Our Strategy: Rank + Truncate
1. **Rank** — Only use the top 3 chunks (already sorted by relevance score from hybrid search)
2. **Truncate** — If any chunk exceeds the remaining budget, it is cut to fit

This keeps the prompt safe, fast, and within limits at all times.

| Metric | Value |
|---|---|
| Context token budget | 1,000 tokens |
| Approximate characters | ~4,000 characters |
| Chunks used per query | Top 3 |
| Token estimation method | 1 token ≈ 4 characters |

---

## Task 3 – Experiments

We ran **2 queries** through all 3 prompts and compared the outputs.

### Experiment 1 — Budget/PDF Query
**Query:** `"What is the inflation target for 2025?"`  
**Source used:** 2025 Ghana Budget PDF

| Prompt | Behaviour Observed |
|---|---|
| Strict | Gave a direct, short factual answer. Refused to add extra details. |
| Loose | Gave a longer, more conversational explanation. |
| Academic | Cited [Source 1], used formal language, structured paragraphs. |

### Experiment 2 — Election/CSV Query
**Query:** `"How many votes did Nana Addo get in the Ahafo region in 2020?"`  
**Source used:** Ghana Presidential Election CSV

| Prompt | Behaviour Observed |
|---|---|
| Strict | Returned exact number from context, nothing else. |
| Loose | Added context about the election year and percentage. |
| Academic | Cited the source chunk and used formal phrasing. |

---

## Key Findings

| Finding | Explanation |
|---|---|
| Prompt A best prevents hallucination | The strict instruction forces the model to say "I don't know" instead of guessing |
| Prompt B gives most readable answers | Natural language, feels like a real assistant |
| Prompt C best for academic work | Citations make answers verifiable and traceable |
| Context window stays within 1,000 tokens | All queries were within budget — no truncation needed for these examples |
| Same context, different prompt = different output | This proves prompt wording matters enormously |

---

## Files in This Part

| File | Description |
|---|---|
| `part_c_prompt_engineering.ipynb` | Main notebook with all tasks and experiments |
| `Part_C_Summary.md` | This summary document |

---

## What Comes Next — Part D

Part D will combine everything:
- Part A chunks → fed into Part B retrieval → Part C prompts → sent to Groq LLM
- Wrapped in a **Streamlit** web app so anyone can type a question and get an answer in real-time
