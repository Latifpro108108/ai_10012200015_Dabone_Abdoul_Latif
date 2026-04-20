import json
import os
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv

class RAGSearch:
    def __init__(self, index_path=None):
        # 1. Load Chunks (Very efficient)
        print("Loading chunks into memory...")
        with open('chunks/csv_chunks.json', 'r') as f:
            csv_chunks = json.load(f)
        with open('chunks/pdf_chunks.json', 'r') as f:
            pdf_chunks = json.load(f)
        self.all_chunks = csv_chunks + pdf_chunks
        
        # 2. Setup BM25 (Zero-RAM Keyword Engine)
        print("Initializing Keyword Search Engine...")
        texts = [c['text'] for c in self.all_chunks]
        tokenized_corpus = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query, k=8):
        """Ultra-lightweight search that fits on Free Tiers."""
        # Get scores for the query
        scores = self.bm25.get_scores(query.lower().split())
        
        # Get top K results
        top_n = np.argsort(scores)[::-1][:k]
        
        results = []
        for i in top_n:
            if scores[i] > 0:
                results.append({
                    'chunk': self.all_chunks[i],
                    'score': float(scores[i])
                })
        return results

class TriangulatorEngine(RAGSearch):
    """
    Smarter Cloud-Native Engine.
    Uses BM25 for rapid retrieval and Groq for intelligent synthesis.
    """
    ELECTION_SIGNALS = ["election", "vote", "winner", "won", "npp", "ndc", "party", "region", "nana", "mahama", "bawumia"]
    BUDGET_SIGNALS = ["budget", "expenditure", "revenue", "gdp", "inflation", "cedi", "ghc", "growth", "fiscal"]

    def _detect_domain(self, query: str) -> str:
        q = query.lower()
        if any(kw in q for kw in self.ELECTION_SIGNALS): return "election"
        if any(kw in q for kw in self.BUDGET_SIGNALS): return "budget"
        return "general"

    def triangulate(self, client, query: str) -> dict:
        domain = self._detect_domain(query)
        
        # Retrieve evidence (Fast & Light)
        results = self.search(query, k=8)
        context = "\n".join([f"[Source: {r['chunk']['source']}] {r['chunk']['text']}" for r in results])
        
        system_prompt = (
            "You are the Academic City AI, a highly intelligent assistant for Ghana government and election data. "
            "Your goal is to provide CLEAR, DIRECT, and HELPFUL answers based on the provided documents.\n\n"
            "RULES:\n"
            "1. ALWAYS prioritize the most recent data (e.g., 2020) over older data.\n"
            "2. If the user asks for a figure, be precise.\n"
            "3. If information is missing, politely say so based on your context."
        )
        
        user_prompt = f"Context Evidence:\n{context}\n\nUser Question: {query}\nHelpful Answer:"
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        ans = response.choices[0].message.content
        conf_level = "HIGH" if len(results) > 3 else "MEDIUM"

        return {
            "final_answer": ans,
            "detected_domain": domain,
            "confidence": {"level": conf_level, "reason": f"Analyzed {len(results)} relevant data points."},
            "sources": results
        }

import numpy as np # Needed for search
