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
    page_title="Ghana RAG AI Assistant",
    page_icon="🇬🇭",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatFloatingInputContainer { background-color: #ffffff; }
    .ghana-header { color: #ce1126; font-weight: bold; }
    .confidence-high   { background:#d4edda; color:#155724; border-radius:8px; padding:8px 14px; font-weight:bold; display:inline-block; }
    .confidence-medium { background:#fff3cd; color:#856404; border-radius:8px; padding:8px 14px; font-weight:bold; display:inline-block; }
    .confidence-low    { background:#f8d7da; color:#721c24; border-radius:8px; padding:8px 14px; font-weight:bold; display:inline-block; }
    </style>
    """, unsafe_allow_html=True)

# --- RESOURCE LOADING ---
@st.cache_resource
def load_all_assets():
    load_dotenv()
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    engine = TriangulatorEngine(index_path='indexes/rag_index.faiss')
    return client, engine

try:
    client, engine = load_all_assets()
except Exception as e:
    st.error(f"Critical Error Loading Project: {e}")
    st.stop()

# --- CONFIDENCE BADGE HELPER ---
def confidence_badge(level: str) -> str:
    icons = {"HIGH": "✅", "MEDIUM": "⚠️", "LOW": "❌"}
    css   = {"HIGH": "confidence-high", "MEDIUM": "confidence-medium", "LOW": "confidence-low"}
    icon  = icons.get(level, "❓")
    cls   = css.get(level, "confidence-medium")
    return f'<span class="{cls}">{icon} {level} CONFIDENCE</span>'

# --- UI LAYOUT ---
st.sidebar.image("https://img.icons8.com/color/96/ghana.png", width=60)
st.sidebar.title("🇬🇭 RAG Project")
st.sidebar.info(f"""
**Student:** Dabone Abdoul Latif  
**Index:** 10012200015  
**Course:** CS4241 - Intro to AI
""")

st.sidebar.markdown("---")
st.sidebar.subheader("System Capabilities")
st.sidebar.write("✅ Hybrid Search (FAISS + BM25)")
st.sidebar.write("✅ Llama 3.3 70B (Groq)")
st.sidebar.write("✅ Anti-Hallucination Prompting")
st.sidebar.write("🆕 Evidence Triangulation (Part G)")
st.sidebar.write("🆕 Domain-Aware Confidence Scoring")

st.sidebar.markdown("---")
st.sidebar.subheader("Part G: Innovation Mode")
use_triangulator = st.sidebar.toggle(
    "🔬 Enable Evidence Triangulation",
    value=False,
    help=(
        "Runs 3 independent retrieval paths and cross-checks answers "
        "for a confidence score. Slower but more trustworthy."
    )
)

st.title("Ghana National Data Chatbot")
st.markdown("Query the **2025 Budget** and **Election Results** with grounded AI.")

if use_triangulator:
    st.info(
        "🔬 **Innovation Mode Active** — Evidence Triangulation Engine is running. "
        "Each query is answered by 3 independent paths and cross-checked for confidence.",
        icon="🆕"
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

# Chat input
if query := st.chat_input("Ask about inflation, GDP, or election winners..."):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    if use_triangulator:
        # ============================================================
        # PART G: Evidence Triangulation Mode
        # ============================================================
        with st.spinner("🔬 Running 3 independent retrieval paths and arbitrating confidence..."):
            report = engine.triangulate(client, query)

        conf  = report["confidence"]
        level = conf["level"]
        badge = confidence_badge(level)

        with st.chat_message("assistant"):
            st.markdown(f"**Answer:** {report['final_answer']}")
            st.markdown(badge, unsafe_allow_html=True)
            st.caption(f"🔎 Detected domain: **{report['detected_domain'].upper()}** | {conf['reason']}")

            with st.expander("🔬 View Full Triangulation Report"):
                tabs = st.tabs(["Path 1: Semantic", "Path 2: Keyword", "Path 3: Domain-Filtered"])

                path_keys = ["semantic", "keyword", "domain_filtered"]
                for tab, key in zip(tabs, path_keys):
                    with tab:
                        path_data = report["paths"][key]
                        st.markdown(f"**Answer:** {path_data['answer']}")
                        st.markdown("**Retrieved Chunks:**")
                        for i, r in enumerate(path_data["chunks"]):
                            st.write(f"Chunk {i+1} | Score: `{r['score']:.4f}` | Source: `{r['chunk']['source']}`")
                            st.caption(r['chunk']['text'][:200] + "...")

                st.divider()
                st.markdown(f"**Arbiter Verdict:** {badge}", unsafe_allow_html=True)
                st.markdown(f"**Reason:** {conf['reason']}")

        answer_display = f"{report['final_answer']}\n\n{badge}"
        st.session_state.messages.append({"role": "assistant", "content": answer_display})

    else:
        # ============================================================
        # Standard RAG Pipeline (original behaviour)
        # ============================================================
        with st.spinner("Analyzing documents..."):
            results = engine.search(query, k=3)
            context = "\n".join(
                f"[Source: {r['chunk']['source']}] {r['chunk']['text']}"
                for r in results
            )
            prompt = (
                "Answer based ONLY on context. "
                "If not found, say you don't know.\n"
                f"Documents: {context}\nQuery: {query}\nAnswer:"
            )
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            answer = resp.choices[0].message.content

        with st.chat_message("assistant"):
            st.markdown(answer)
            with st.expander("🔍 View RAG Pipeline Inspector"):
                st.write("### 1. Retrieved Chunks (Hybrid Scoring)")
                for i, r in enumerate(results):
                    st.write(f"**Chunk {i+1}** | Score: `{r['score']:.4f}` | Source: `{r['chunk']['source']}`")
                    st.caption(f"Text snippet: {r['chunk']['text'][:200]}...")
                st.divider()
                st.write("### 2. Final Prompt (Grounded Context)")
                st.code(prompt, language="markdown")

        st.session_state.messages.append({"role": "assistant", "content": answer})

# Footnote
st.markdown("---")
st.caption("Developed for Academic City University College | CS4241 Introduction to Artificial Intelligence")
