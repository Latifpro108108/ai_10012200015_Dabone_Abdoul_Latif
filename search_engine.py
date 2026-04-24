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

    def search(self, query, k=5, alpha=0.5):
        # Semantic search
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


class TriangulatorEngine(RAGSearch):
    def triangulate(self, client, query: str) -> dict:
        # Use a high-quality hybrid search (The "Smart" Path)
        results = self.search(query, k=6, alpha=0.6)
        
        if not results:
            return {
                "final_answer": "I'm sorry, I couldn't find any specific information in the documents regarding that question.",
                "confidence": {"level": "LOW", "reason": "No relevant document chunks found."},
                "sources": []
            }

        context = "\n".join([f"[Source: {r['chunk']['source']}] {r['chunk']['text']}" for r in results])
        
        # SMART & HELPFUL PROMPT
        system_prompt = (
            "You are the Ghana Intel Assistant, an expert on the 2025 Budget and 2020 Elections. "
            "Your goal is to be EXTREMELY HELPFUL, SMART, and DESCRIPTIVE. "
            "Use the provided context to answer the user's question in a professional and conversational tone.\n\n"
            "RULES:\n"
            "1. If you find multiple related facts, synthesize them into a comprehensive answer.\n"
            "2. If the answer isn't explicitly there but you have related info, explain what you found.\n"
            "3. Be confident and clear."
        )
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context Evidence:\n{context}\n\nQuestion: {query}"}
            ],
            temperature=0.3 # Slightly higher for more "natural" and "smart" sounding answers
        )
        
        ans = response.choices[0].message.content
        
        return {
            "final_answer": ans,
            "confidence": {"level": "HIGH", "reason": f"Analyzed {len(results)} source chunks for a comprehensive answer."},
            "sources": results
        }
