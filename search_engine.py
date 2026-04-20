import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

class RAGSearch:
    def __init__(self, index_path='indexes/rag_index.faiss'):
        # 1. Load Chunks
        with open('chunks/csv_chunks.json', 'r') as f:
            csv_chunks = json.load(f)
        with open('chunks/pdf_chunks.json', 'r') as f:
            pdf_chunks = json.load(f)
        self.all_chunks = csv_chunks + pdf_chunks
        
        # 2. Load Model & Index
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index(index_path)
        
        # 3. Setup BM25
        texts = [c['text'] for c in self.all_chunks]
        tokenized_corpus = [text.lower().split() for text in texts]
        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query, k=5, alpha=0.5):
        """Enhanced search with higher k to ensure recent data is caught."""
        # Vector search
        query_vec = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vec, k * 2)
        
        # BM25 search
        bm25_scores = self.bm25.get_scores(query.lower().split())
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        
        combined = []
        for i, chunk in enumerate(self.all_chunks):
            v_score = 0
            for rank, idx in enumerate(indices[0]):
                if idx == i:
                    v_score = 1 / (1 + distances[0][rank])
                    break
            
            score = (alpha * v_score) + ((1 - alpha) * (bm25_scores[i] / max_bm25))
            if score > 0:
                combined.append({'chunk': chunk, 'score': score})
                
        return sorted(combined, key=lambda x: x['score'], reverse=True)[:k]


# =============================================================================
# PART G INNOVATION: Smart Evidence Synthesis Engine
# =============================================================================

class TriangulatorEngine(RAGSearch):
    """
    Smarter Innovation: Evidence Synthesis with Domain Intelligence.
    
    This engine retrieves data from multiple perspectives but focuses on 
    SYNTHESIZING a helpful answer rather than being a strict filter.
    """

    ELECTION_SIGNALS = ["election", "vote", "winner", "won", "npp", "ndc", "party", "region", "nana", "mahama", "bawumia"]
    BUDGET_SIGNALS = ["budget", "expenditure", "revenue", "gdp", "inflation", "cedi", "ghc", "growth", "fiscal"]

    def _detect_domain(self, query: str) -> str:
        q = query.lower()
        if any(kw in q for kw in self.ELECTION_SIGNALS): return "election"
        if any(kw in q for kw in self.BUDGET_SIGNALS): return "budget"
        return "general"

    def triangulate(self, client, query: str) -> dict:
        """
        Retrieves evidence from Semantic, Keyword, and Domain paths,
        then synthesizes them into one highly intelligent response.
        """
        domain = self._detect_domain(query)
        
        # 1. Gather Broad Evidence
        semantic_path = self.search(query, k=4, alpha=0.8) # Favor meaning
        keyword_path  = self.search(query, k=4, alpha=0.2) # Favor exact figures
        
        # Combine and deduplicate chunks
        unique_chunks = {}
        for r in semantic_path + keyword_path:
            text = r['chunk']['text']
            if text not in unique_chunks or r['score'] > unique_chunks[text]['score']:
                unique_chunks[text] = r
        
        results = sorted(unique_chunks.values(), key=lambda x: x['score'], reverse=True)[:6]
        
        # 2. Smart Synthesis Prompt
        context = "\n".join([f"[Source: {r['chunk']['source']}] {r['chunk']['text']}" for r in results])
        
        system_prompt = (
            "You are the Academic City AI, a highly intelligent assistant for Ghana government and election data. "
            "Your goal is to provide CLEAR, DIRECT, and HELPFUL answers based on the provided documents.\n\n"
            "RULES:\n"
            "1. If multiple years or versions of data exist (e.g. 2012 vs 2020), always prioritize the MOST RECENT data unless the user asks for a specific year.\n"
            "2. Do not say 'NOT_FOUND' if you can find a partial or related answer. Be helpful like a real assistant.\n"
            "3. If the answer is absolutely not there, politely explain what data you DO have.\n"
            "4. For election queries, identify the candidate and their specific results (votes/percentage) clearly."
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
        
        # 3. Simple Confidence Check
        # If the LLM's answer is short or contains "I don't know", confidence is low.
        ans = response.choices[0].message.content
        conf_level = "HIGH"
        if len(results) < 2 or "not mentioned" in ans.lower() or "don't know" in ans.lower():
            conf_level = "MEDIUM"
        if "not found" in ans.lower():
            conf_level = "LOW"

        return {
            "final_answer": ans,
            "detected_domain": domain,
            "confidence": {"level": conf_level, "reason": f"Synthesized from {len(results)} relevant sources."},
            "sources": results
        }
