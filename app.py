import streamlit as st
import json
import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from groq import Groq
from dotenv import load_dotenv
from search_engine import TriangulatorEngine

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Ghana Intel AI",
    page_icon="🇬🇭",
    layout="wide"
)

# --- PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background-color: #0a0a0a; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #CE1126; }
    
    .answer-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 30px;
        border-left: 5px solid #FCD116;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .ghana-text {
        background: linear-gradient(to right, #CE1126, #FCD116, #006B3F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
    }
    
    .badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: bold;
        background: #006B3F;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ASSETS ---
@st.cache_resource
def load_assets():
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    engine = TriangulatorEngine(index_path='indexes/rag_index.faiss')
    return client, engine

client, engine = load_assets()

# --- SIDEBAR ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)
    else:
        st.image("https://img.icons8.com/color/144/ghana.png", width=70)
    
    st.markdown("<h2 style='color:white;'>Ghana Intelligence</h2>", unsafe_allow_html=True)
    st.info(f"**Dabone Abdoul Latif**\n\nIndex: `10012200015`\n\nCS4241 - Intro to AI")
    st.divider()
    st.caption("v3.0 | Smart RAG Enabled")

# --- MAIN ---
st.markdown("<div class='ghana-text'>Ghana Data Intel</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#888;'>Smart AI Assistant for the 2025 Budget & 2020 Elections.</p>", unsafe_allow_html=True)

query = st.chat_input("Ask a question...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents..."):
            report = engine.triangulate(client, query)
            
        # Display the Main Smart Answer
        st.markdown(f"""
            <div class="answer-card">
                <div style="margin-bottom:10px;"><span class="badge">SMART ANSWER</span></div>
                <p style="font-size:1.15rem; line-height:1.6;">{report['final_answer']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Evidence Drop-down
        with st.expander("📂 View Source Evidence (Chunks)"):
            for i, r in enumerate(report['sources']):
                st.markdown(f"**Source {i+1}** | Score: `{r['score']:.4f}` | {r['chunk']['source']}")
                st.caption(r['chunk']['text'])
                st.divider()
