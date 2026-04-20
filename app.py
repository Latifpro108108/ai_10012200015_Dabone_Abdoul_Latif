import streamlit as st
import json
import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from groq import Groq
from dotenv import load_dotenv

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ghana RAG AI Assistant",
    page_icon="🇬🇭",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatFloatingInputContainer { background-color: #ffffff; }
    .st-emotion-cache-1c7n2ka { background-color: #ffffff; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .ghana-header { color: #ce1126; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- RESOURCE LOADING ---
@st.cache_resource
def load_all_assets():
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    # Load chunks
    with open('chunks/csv_chunks.json', 'r') as f: csv_chunks = json.load(f)
    with open('chunks/pdf_chunks.json', 'r') as f: pdf_chunks = json.load(f)
    all_chunks = csv_chunks + pdf_chunks
    
    # Load retrieval models
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index('indexes/rag_index.faiss')
    
    # Build BM25
    texts = [c['text'] for c in all_chunks]
    bm25 = BM25Okapi([t.lower().split() for t in texts])
    
    return client, all_chunks, model, index, bm25

try:
    client, all_chunks, model, index, bm25 = load_all_assets()
except Exception as e:
    st.error(f"Critical Error Loading Project: {e}")
    st.stop()

# --- PIPELINE LOGIC ---
def run_pipeline(query, k=3):
    # Stage 1: Retrieval
    query_vec = model.encode([query]).astype('float32')
    distances, indices = index.search(query_vec, k * 2)
    bm25_scores = bm25.get_scores(query.lower().split())
    max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
    
    combined = []
    for i, chunk in enumerate(all_chunks):
        v_score = 0
        for rank, idx in enumerate(indices[0]):
            if idx == i: v_score = 1 / (1 + distances[0][rank])
        score = (0.5 * v_score) + (0.5 * (bm25_scores[i] / max_bm25))
        if score > 0: combined.append({'chunk': chunk, 'score': score})
    
    results = sorted(combined, key=lambda x: x['score'], reverse=True)[:k]
    
    # Stage 2 & 3: Context and Prompt
    context = "".join([f"\n[Source: {r['chunk']['source']}] {r['chunk']['text']}\n" for r in results])
    prompt = f"Answer based ONLY on context. If not found, say you don't know.\nDocuments: {context}\nQuery: {query}\nAnswer:"
    
    # Stage 4: LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return results, prompt, response.choices[0].message.content

# --- UI LAYOUT ---
st.sidebar.image("https://img.icons8.com/color/96/ghana.png", width=60)
st.sidebar.title("🇬🇭 RAG Project")
st.sidebar.info(f"""
**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Intro to AI
""")

st.sidebar.markdown("---")
st.sidebar.subheader("Project Specs")
st.sidebar.write("✅ Hybrid Search (FAISS + BM25)")
st.sidebar.write("✅ Llama 3.3 70B (Groq)")
st.sidebar.write("✅ Anti-Hallucination Prompting")

st.title("Ghana National Data Chatbot")
st.markdown("Query the **2025 Budget** and **Election Results** with grounded AI.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if query := st.chat_input("Ask about inflation, GDP, or election winners..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Analyzing documents..."):
        results, final_prompt, answer = run_pipeline(query)

    with st.chat_message("assistant"):
        st.markdown(answer)
        
        # Display Pipeline Inspector
        with st.expander("🔍 View RAG Pipeline Inspector"):
            st.write("### 1. Retrieved Chunks (Hybrid Scoring)")
            for i, r in enumerate(results):
                st.write(f"**Chunk {i+1}** | Score: `{r['score']:.4f}` | Source: `{r['chunk']['source']}`")
                st.caption(f"Text snippet: {r['chunk']['text'][:200]}...")
            
            st.divider()
            st.write("### 2. Final Prompt (Grounded Context)")
            st.code(final_prompt, language="markdown")

    st.session_state.messages.append({"role": "assistant", "content": answer})

# Footnote
st.markdown("---")
st.caption("Developed for Academic City University College | CS4241 Introduction to Artificial Intelligence")
