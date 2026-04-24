import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import ssl

# Fix SSL Certificate Error on Windows
ssl._create_default_https_context = ssl._create_unverified_context

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

    def search(self, query, k=5, alpha=0.5, source_filter=None):
        if source_filter:
            filtered_indices = [i for i, c in enumerate(self.all_chunks) if source_filter.lower() in c['source'].lower()]
            if not filtered_indices: return []
        else:
            filtered_indices = list(range(len(self.all_chunks)))

        query_vec = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vec, k * 5)
        
        bm25_scores = self.bm25.get_scores(query.lower().split())
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        
        combined = []
        for i in filtered_indices:
            v_score = 0
            for rank, idx in enumerate(indices[0]):
                if idx == i:
                    v_score = 1 / (1 + distances[0][rank])
                    break
            score = (alpha * v_score) + ((1 - alpha) * (bm25_scores[i] / max_bm25))
            if score > 0:
                combined.append({'chunk': self.all_chunks[i], 'score': score})
        return sorted(combined, key=lambda x: x['score'], reverse=True)[:k]

class TriangulatorEngine(RAGSearch):
    def _detect_domain(self, query: str) -> str:
        q = query.lower()
        election_signals = ["election", "vote", "winner", "won", "npp", "ndc", "party", "region"]
        budget_signals = ["budget", "expenditure", "revenue", "gdp", "inflation", "cedi", "ghc"]
        if any(kw in q for kw in election_signals): return "election"
        if any(kw in q for kw in budget_signals): return "budget"
        return "general"

    def _domain_filtered_search(self, query, k=3):
        domain = self._detect_domain(query)
        source_gate = "csv" if domain == "election" else "pdf" if domain == "budget" else None
        return self.search(query, k=k, alpha=0.5, source_filter=source_gate)

    def _get_path_answer(self, client, query, results):
        if not results: return "NOT_FOUND"
        context = "\n".join([f"[Source: {r['chunk']['source']}] {r['chunk']['text']}" for r in results])
        prompt = f"Answer concisely based ONLY on this context. If not found, say NOT_FOUND.\nContext:\n{context}\nQuery: {query}\nAnswer:"
        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return resp.choices[0].message.content
        except:
            return "Answer unavailable"

    def triangulate(self, client, query: str) -> dict:
        domain = self._detect_domain(query)
        
        # Run the 3 independent paths (Unique evidence for the Notebook)
        p1_res = self.search(query, k=3, alpha=1.0)
        p1_ans = self._get_path_answer(client, query, p1_res)

        p2_res = self.search(query, k=3, alpha=0.0)
        p2_ans = self._get_path_answer(client, query, p2_res)

        p3_res = self._domain_filtered_search(query, k=3)
        p3_ans = self._get_path_answer(client, query, p3_res)

        # Smart Final Synthesis (The "Smart" Result for the User)
        all_results = self.search(query, k=6, alpha=0.6)
        context = "\n".join([f"[Source: {r['chunk']['source']}] {r['chunk']['text']}" for r in all_results])
        
        final_prompt = (
            "You are the Ghana Intel Assistant. Synthesize the provided evidence into a smart, descriptive answer.\n"
            f"Context:\n{context}\n\nQuestion: {query}"
        )
        final_resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": final_prompt}],
            temperature=0.3
        )
        final_ans = final_resp.choices[0].message.content

        # Determine confidence based on consensus
        conf_level = "HIGH"
        if p1_ans == "NOT_FOUND" and p2_ans == "NOT_FOUND":
            conf_level = "LOW"
        elif p1_ans == "NOT_FOUND" or p2_ans == "NOT_FOUND":
            conf_level = "MEDIUM"

        return {
            "final_answer": final_ans,
            "detected_domain": domain,
            "confidence": {"level": conf_level, "reason": f"Synthesized from {len(all_results)} verified evidence chunks."},
            "paths": {
                "semantic": {"answer": p1_ans, "chunks": p1_res},
                "keyword": {"answer": p2_ans, "chunks": p2_res},
                "domain_filtered": {"answer": p3_ans, "chunks": p3_res}
            },
            "sources": all_results
        }
