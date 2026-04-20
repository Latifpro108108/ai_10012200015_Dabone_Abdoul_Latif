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

    def search(self, query, k=3, alpha=0.5):
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
