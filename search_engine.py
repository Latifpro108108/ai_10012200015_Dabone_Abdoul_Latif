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


# =============================================================================
# PART G INNOVATION: Evidence Triangulation Engine (Domain-Specific Confidence)
# =============================================================================

class TriangulatorEngine(RAGSearch):
    """
    Novel Innovation: Evidence Triangulation with Domain-Aware Confidence Scoring.

    Instead of a single retrieval pass, this engine runs THREE independent
    retrieval paths and cross-checks the answers for consistency:

        Path 1 -> Pure Semantic Search (FAISS only, alpha=1.0)
        Path 2 -> Pure Keyword Search  (BM25 only,  alpha=0.0)
        Path 3 -> Domain-Filtered Search (source-type gated by query intent)

    The LLM answers each path independently. A final "Arbiter" LLM call
    compares all three answers and assigns a CONFIDENCE LEVEL:
        HIGH   -- all 3 paths agree         (answer is reliable)
        MEDIUM -- 2 of 3 paths agree        (answer is probably correct)
        LOW    -- all 3 paths disagree      (flag answer as unreliable)

    This is domain-specific because the Domain Filter understands that
    "election" queries should NOT pull budget chunks, and vice versa,
    making it uniquely suited to the Ghana Government data domain.
    """

    # Keywords that signal a query is about elections/politics
    ELECTION_SIGNALS = [
        "election", "vote", "voting", "winner", "won", "candidate",
        "npp", "ndc", "party", "parliament", "presidential", "constituency",
        "results", "polling", "ballot", "region", "district"
    ]

    # Keywords that signal a query is about the government budget/economy
    BUDGET_SIGNALS = [
        "budget", "expenditure", "revenue", "gdp", "inflation", "debt",
        "fiscal", "economy", "spending", "deficit", "surplus", "tax",
        "billion", "million", "cedi", "ghc", "growth", "finance",
        "allocation", "infrastructure", "education", "health"
    ]

    def _detect_domain(self, query: str) -> str:
        """
        Classifies the query as 'election', 'budget', or 'mixed'
        based on keyword signals. Returns the dominant domain.
        """
        q = query.lower()
        election_hits = sum(1 for kw in self.ELECTION_SIGNALS if kw in q)
        budget_hits   = sum(1 for kw in self.BUDGET_SIGNALS   if kw in q)

        if election_hits > budget_hits:
            return "election"
        elif budget_hits > election_hits:
            return "budget"
        else:
            return "mixed"

    def _semantic_search(self, query: str, k: int = 3) -> list:
        """Path 1: Pure FAISS vector / semantic search (alpha = 1.0)."""
        return self.search(query, k=k, alpha=1.0)

    def _keyword_search(self, query: str, k: int = 3) -> list:
        """Path 2: Pure BM25 keyword search (alpha = 0.0)."""
        return self.search(query, k=k, alpha=0.0)

    def _domain_filtered_search(self, query: str, k: int = 3) -> list:
        """
        Path 3: Hybrid search but filtered to only chunks from the
        detected domain source (budget PDF or elections CSV).
        """
        domain = self._detect_domain(query)
        query_vec = self.model.encode([query]).astype('float32')
        distances, indices = self.index.search(query_vec, len(self.all_chunks))

        bm25_scores = self.bm25.get_scores(query.lower().split())
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1

        combined = []
        for i, chunk in enumerate(self.all_chunks):
            # --- Domain Gate ---
            source = chunk.get('source', '').lower()
            if domain == "election" and "budget" in source:
                continue  # skip budget chunks for election queries
            if domain == "budget" and ("election" in source or "csv" in source):
                continue  # skip election chunks for budget queries
            # 'mixed' -> no filter, use all chunks

            v_score = 0
            for rank, idx in enumerate(indices[0]):
                if idx == i:
                    v_score = 1 / (1 + distances[0][rank])
                    break

            score = (0.5 * v_score) + (0.5 * (bm25_scores[i] / max_bm25))
            if score > 0:
                combined.append({'chunk': chunk, 'score': score})

        return sorted(combined, key=lambda x: x['score'], reverse=True)[:k]

    def _chunks_to_context(self, results: list) -> str:
        """Helper: format retrieved chunks into a prompt context block."""
        return "\n".join(
            f"[Source: {r['chunk']['source']}] {r['chunk']['text']}"
            for r in results
        )

    def _ask_llm(self, client, context: str, query: str) -> str:
        """Helper: call Groq LLM with a strict grounding prompt."""
        prompt = (
            "You are a strict factual assistant. Answer ONLY from the provided context. "
            "If the answer is not present, respond exactly: NOT_FOUND\n\n"
            f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
        )
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300
        )
        return resp.choices[0].message.content.strip()

    def _compute_confidence(self, client, ans1: str, ans2: str, ans3: str) -> dict:
        """
        Arbiter step: asks the LLM to compare the three independent answers
        and return a structured consistency verdict.
        Returns a dict with 'level' (HIGH|MEDIUM|LOW), 'reason', and 'best_answer'.
        """
        arbiter_prompt = (
            "You are an impartial evidence arbiter. Three independent AI retrievers "
            "answered the same question:\n\n"
            f"Answer A (Semantic Path):       {ans1}\n"
            f"Answer B (Keyword Path):        {ans2}\n"
            f"Answer C (Domain-Filtered Path):{ans3}\n\n"
            "Task: Compare these answers and decide:\n"
            "- HIGH:   All three answers convey the same factual information.\n"
            "- MEDIUM: Two of three answers agree; one is different or says NOT_FOUND.\n"
            "- LOW:    All three answers are different or most say NOT_FOUND.\n\n"
            "Respond in this EXACT format (no extra lines):\n"
            "CONFIDENCE: <HIGH|MEDIUM|LOW>\n"
            "REASON: <one sentence>\n"
            "BEST_ANSWER: <the most accurate answer, or NOT_FOUND>"
        )
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": arbiter_prompt}],
            temperature=0,
            max_tokens=300
        )
        raw = resp.choices[0].message.content.strip()

        # Parse the structured response
        result = {
            "level": "MEDIUM",
            "reason": "Could not parse arbiter output.",
            "best_answer": ans1
        }
        for line in raw.split("\n"):
            if line.startswith("CONFIDENCE:"):
                lvl = line.replace("CONFIDENCE:", "").strip().upper()
                if lvl in ("HIGH", "MEDIUM", "LOW"):
                    result["level"] = lvl
            elif line.startswith("REASON:"):
                result["reason"] = line.replace("REASON:", "").strip()
            elif line.startswith("BEST_ANSWER:"):
                result["best_answer"] = line.replace("BEST_ANSWER:", "").strip()

        return result

    def triangulate(self, client, query: str, k: int = 3) -> dict:
        """
        Main public entry point.
        Runs all three retrieval paths, collects independent LLM answers,
        arbitrates, and returns a complete triangulation report dict.
        """
        domain = self._detect_domain(query)

        # --- Step 1: Run 3 independent retrieval paths ---
        path1_chunks = self._semantic_search(query, k)
        path2_chunks = self._keyword_search(query, k)
        path3_chunks = self._domain_filtered_search(query, k)

        # --- Step 2: Get independent LLM answers ---
        ans1 = self._ask_llm(client, self._chunks_to_context(path1_chunks), query)
        ans2 = self._ask_llm(client, self._chunks_to_context(path2_chunks), query)
        ans3 = self._ask_llm(client, self._chunks_to_context(path3_chunks), query)

        # --- Step 3: Arbitration & Confidence Scoring ---
        confidence = self._compute_confidence(client, ans1, ans2, ans3)

        return {
            "query":            query,
            "detected_domain":  domain,
            "paths": {
                "semantic":        {"chunks": path1_chunks, "answer": ans1},
                "keyword":         {"chunks": path2_chunks, "answer": ans2},
                "domain_filtered": {"chunks": path3_chunks, "answer": ans3},
            },
            "confidence":  confidence,
            "final_answer": confidence["best_answer"],
        }
