import os
import time
import hashlib
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import ArxivLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()
OPENALEX_API_KEY = os.getenv("OPENALEX_API_KEY")

st.set_page_config(page_title="RABOT · Research Assistant", page_icon="◈", layout="wide")

# ============================================================
# THEME — "Obsidian & Amber": ink-black surfaces, warm amber
# primary accent, iris-violet secondary glow.
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&display=swap');
:root{--bg:#0A0B10;--surface:#12141C;--surface2:#181B26;--line:#232736;
--amber:#F2B15C;--iris:#8B7CFF;--text:#E8E6E1;--muted:#8A8FA3;}
html,body,[class*="css"],.stApp{font-family:'Inter',sans-serif;color:var(--text);}
.stApp{background:radial-gradient(900px 500px at 85% -10%,rgba(139,124,255,.14),transparent 60%),
radial-gradient(700px 400px at -5% 10%,rgba(242,177,92,.10),transparent 60%),var(--bg);}
header[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"],[data-testid="stDecoration"],#MainMenu,footer{visibility:hidden;}
.block-container{padding-top:2rem;max-width:1100px;}
section[data-testid="stSidebar"]{background:var(--surface);border-right:1px solid var(--line);}
h1,h2,h3{font-family:'Fraunces',serif!important;letter-spacing:-.01em;}
.brand{display:flex;align-items:center;gap:.6rem;margin-bottom:.2rem}
.brand .logo{width:34px;height:34px;border-radius:10px;display:grid;place-items:center;font-size:18px;color:#0A0B10;
background:linear-gradient(135deg,var(--amber),#F7D59A);box-shadow:0 0 22px rgba(242,177,92,.35)}
.brand .name{font-family:'Fraunces',serif;font-size:1.5rem;font-weight:700}
.tag{color:var(--muted);font-size:.82rem;margin-bottom:1.2rem}
.hero{padding:3.2rem 0 1rem;text-align:center;animation:rise .8s ease both}
.hero h1{font-size:3.1rem;line-height:1.1;margin:0 0 .7rem}
.hero h1 span{background:linear-gradient(90deg,var(--amber),var(--iris));-webkit-background-clip:text;color:transparent}
.hero p{color:var(--muted);max-width:560px;margin:0 auto}
.card{background:linear-gradient(180deg,var(--surface2),var(--surface));border:1px solid var(--line);border-radius:14px;
padding:1rem 1.2rem;margin-bottom:.35rem;transition:all .25s ease;animation:rise .5s ease both}
.card:hover{border-color:rgba(242,177,92,.55);transform:translateY(-2px);box-shadow:0 10px 30px rgba(0,0,0,.4)}
.card .t{font-weight:600;font-size:1rem;line-height:1.35}
.card .m{color:var(--muted);font-size:.8rem;margin-top:.35rem}
.pill{display:inline-block;padding:.12rem .55rem;border-radius:99px;font-size:.7rem;margin-right:.4rem;
border:1px solid var(--line);color:var(--amber);background:rgba(242,177,92,.07)}
.paperbar{border:1px solid var(--line);border-left:3px solid var(--amber);border-radius:12px;padding:.9rem 1.2rem;
background:var(--surface);margin-bottom:1rem}
.paperbar .t{font-family:'Fraunces',serif;font-size:1.25rem;font-weight:500}
.stat{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.7rem 1rem;text-align:center}
.stat b{display:block;font-size:1.3rem;color:var(--amber);font-family:'Fraunces',serif}
.stat span{font-size:.72rem;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.stButton>button{background:var(--surface2);color:var(--text);border:1px solid var(--line);border-radius:10px;
transition:all .2s ease;font-weight:500}
.stButton>button:hover{border-color:var(--amber);color:var(--amber);box-shadow:0 0 18px rgba(242,177,92,.18)}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--amber),#E69A3E);color:#14100A;border:none;font-weight:600}
.stTextInput input{background:var(--surface2)!important;border:1px solid var(--line)!important;border-radius:10px!important;color:var(--text)!important}
.stTextInput input:focus{border-color:var(--amber)!important;box-shadow:0 0 0 2px rgba(242,177,92,.18)!important}
.stTabs [data-baseweb="tab-list"]{gap:.4rem;border-bottom:1px solid var(--line)}
.stTabs [aria-selected="true"]{color:var(--amber)!important}
.stTabs [data-baseweb="tab-highlight"]{background:var(--amber)!important}
[data-testid="stChatMessage"]{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:.9rem 1rem}
[data-testid="stChatInput"]{border-radius:14px}
.src{font-family:'JetBrains Mono',monospace;font-size:.78rem;color:var(--muted);border-left:2px solid var(--iris);padding-left:.7rem;margin:.5rem 0}
.mobile-hint{display:none;text-align:center;color:var(--amber);font-size:.85rem;border:1px dashed rgba(242,177,92,.4);
border-radius:10px;padding:.5rem;margin:.5rem 0 1rem}
@media (max-width:640px){
.block-container{padding:2.8rem .8rem 4rem}
.hero{padding:1rem 0 .5rem}.hero h1{font-size:2rem}.hero p{font-size:.9rem}
.mobile-hint{display:block}
.paperbar{padding:.7rem .9rem}.paperbar .t{font-size:1.05rem}
[data-testid="stHorizontalBlock"]{flex-wrap:nowrap!important;gap:.5rem!important}
[data-testid="stColumn"]{min-width:0!important}
.stat{padding:.5rem .3rem}.stat b{font-size:1.05rem}.stat span{font-size:.58rem;letter-spacing:.03em}
[data-testid="stChatMessage"]{padding:.6rem}
.card{padding:.8rem .9rem}.card .t{font-size:.92rem}
}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
::-webkit-scrollbar{width:8px}::-webkit-scrollbar-thumb{background:var(--line);border-radius:8px}
</style>
""", unsafe_allow_html=True)

# ============================================================
# Backend
# ============================================================
@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatGroq(model_name="openai/gpt-oss-120b", temperature=0)


@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def search_openalex(query):
    params = {"search": query, "filter": "is_oa:true", "per_page": 5, "api_key": OPENALEX_API_KEY}
    for attempt in range(5):
        try:
            r = requests.get("https://api.openalex.org/works", params=params, timeout=20)
            if r.status_code == 429:
                time.sleep(int(r.headers.get("Retry-After", 2 ** attempt)))
                continue
            r.raise_for_status()
            return r.json().get("results", [])
        except requests.RequestException:
            time.sleep(2 ** attempt)
    return []


def get_arxiv_id(paper):
    for loc in paper.get("locations", []):
        url = loc.get("landing_page_url") or ""
        if "arxiv.org" in url:
            return url.split("/")[-1]
    return None


def safe_arxiv_load(query, retries=3):
    for _ in range(retries):
        try:
            return ArxivLoader(query=query, load_max_docs=1).load()
        except Exception:
            time.sleep(3)
    return []


def paper_path(paper):
    return f"vector_store/{hashlib.md5(paper.get('title', '').encode()).hexdigest()}"


def make_retriever(db):
    return db.as_retriever(search_type="mmr", search_kwargs={"k": 6, "fetch_k": 24})


def build_retriever(paper):
    path = paper_path(paper)
    # Cached: load straight from disk, no arXiv download or re-embedding
    if os.path.exists(path):
        db = Chroma(persist_directory=path, embedding_function=get_embeddings())
        n = db._collection.count()
        if n:
            return make_retriever(db), n, True
    docs = safe_arxiv_load(get_arxiv_id(paper) or paper.get("title", ""))
    if not docs:
        return None, 0, False
    chunks = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100).split_documents(docs)
    os.makedirs("vector_store", exist_ok=True)
    db = Chroma.from_documents(chunks, get_embeddings(), persist_directory=path)
    return make_retriever(db), len(chunks), False


PROMPT = ChatPromptTemplate.from_template("""
You are RABOT, an expert research-paper tutor. Help the reader truly understand the paper.

Rules:
1. Use ONLY the paper context below. Never add outside knowledge or guess. Use the paper's own terms
   exactly as written (do not rename or reinterpret technical terms).
2. If the context does not contain the answer, reply exactly:
   "This information is not available in the paper."
3. Begin with one natural sentence that directly answers the question, phrased as a full statement
   (e.g. "The datasets used in this paper are ...", "The main limitation of the approach is ...").
4. Then give the complete answer: the key points, the reasoning behind them, and any specific numbers,
   names, formulas or results the paper reports. Briefly explain jargon in plain words.
5. Use short bullet points or a small table when it makes things clearer. Stay accurate over long.

Paper context:
{context}

Question:
{Question}

Answer:
""")

SUMMARY_PROMPT = ChatPromptTemplate.from_template("""
You are RABOT, an expert research-paper tutor. Write a clear, complete summary of the paper so that a
reader who has not read it understands what it does, how, and why it matters.

Rules:
- Use ONLY the context below. Do not guess or add outside knowledge. Keep the paper's exact terminology.
- If a section is not covered by the context, write "Not clearly stated in the paper." for that section.
- Start each section with a natural lead-in sentence, then supporting details. Put every heading on its own line,
  exactly as written below (no bold around it), with a blank line before and after. Use exactly this layout:

## Overview
One short paragraph: what the paper is about and the one-line takeaway.

## Problem
Start with "The problem this paper addresses is ..." and explain the gap or motivation.

## Methodology
Start with "The authors propose / approach the problem by ..." then explain the method step by step,
including key ideas, architecture, data and training or evaluation setup, in plain language.

## Key Contributions
Start with "The key contributions of this paper are:" followed by bullets, each with a short explanation.

## Results
Start with "The main results show that ..." and report concrete numbers, comparisons and benchmarks
the paper gives (use a small table if it helps).

## Limitations
Start with "The limitations of this work include ..." (only what the paper states or clearly implies).

## In Simple Words
2-3 sentences a beginner would understand.

Paper context:
{context}

Summary:
""")


SUMMARY_QUERIES = [
    "abstract and main idea of the paper",
    "problem statement, motivation and background",
    "proposed method, architecture and approach",
    "key contributions of this work",
    "experiments, datasets, baselines and evaluation setup",
    "results, performance comparison and findings",
    "limitations, future work and conclusion",
]


def clean_md(text):
    """Turn any '## Title' / '**## Title**' line into a proper heading on its own lines."""
    text = re.sub(r"^[ \t>*_]*#{1,6}[ \t]*(.+?)[ \t*_]*$", r"\n### \1\n", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def generate_summary():
    seen, parts = set(), []
    for q in SUMMARY_QUERIES:
        for d in st.session_state.retriever.invoke(q):
            if d.page_content not in seen:
                seen.add(d.page_content)
                parts.append(d.page_content)
    chain = SUMMARY_PROMPT | get_llm() | StrOutputParser()
    return chain.invoke({"context": "\n\n".join(parts)})


def ask_stream(question):
    docs = st.session_state.retriever.invoke(question)
    context = "\n\n".join(d.page_content for d in docs)
    chain = PROMPT | get_llm() | StrOutputParser()
    return chain.stream({"context": context, "Question": question}), docs


# ============================================================
# State
# ============================================================
for k, v in {"results": [], "paper": None, "retriever": None, "chunks": 0,
             "summary": None, "messages": [], "pending": None}.items():
    st.session_state.setdefault(k, v)


def load_paper(paper):
    with st.status("Preparing paper…", expanded=True) as s:
        st.write("🧠 Loading paper index")
        retriever, n, cached = build_retriever(paper)
        if not retriever:
            s.update(label="Could not load this paper", state="error")
            st.error("No arXiv full text found. Try another result.")
            return
        st.write("⚡ Using saved index" if cached else "📥 Downloaded & indexed from arXiv")
        st.session_state.update(paper=paper, retriever=retriever, chunks=n, messages=[], summary=None)
        summary_file = paper_path(paper) + "_summary.txt"
        if os.path.exists(summary_file):
            st.write("⚡ Using saved summary")
            st.session_state.summary = open(summary_file, encoding="utf-8").read()
        else:
            st.write("✍️ Writing structured summary")
            summary = generate_summary()
            st.session_state.summary = summary
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary)
        s.update(label="Ready", state="complete", expanded=False)


# ============================================================
# Sidebar
# ============================================================
with st.sidebar:
    st.markdown('<div class="brand"><div class="logo">◈</div><div class="name">RABOT</div></div>'
                '<div class="tag">Research Paper Assistant</div>', unsafe_allow_html=True)
    query = st.text_input("Find a paper", placeholder="Title or keywords…", label_visibility="collapsed")
    if st.button("Search papers", type="primary", use_container_width=True):
        if len(query.strip()) < 3:
            st.warning("Enter a more specific query.")
        else:
            with st.spinner("Searching OpenAlex…"):
                st.session_state.results = search_openalex(query.strip())
            if not st.session_state.results:
                st.error("No open-access papers found. Try the exact title.")
    if st.session_state.paper:
        st.divider()
        if st.button("＋ New paper", use_container_width=True):
            st.session_state.update(paper=None, retriever=None, summary=None, messages=[], results=[])
            st.rerun()
        if st.session_state.messages:
            log = "\n\n".join(f"**{m['role'].title()}:** {m['content']}" for m in st.session_state.messages)
            st.download_button("⬇ Export chat", log, file_name="rabot_chat.md", use_container_width=True)
            if st.button("Clear chat", use_container_width=True):
                st.session_state.messages = []
                st.rerun()

# ============================================================
# Main
# ============================================================
paper = st.session_state.paper

if not paper:
    st.markdown('<div class="mobile-hint">☰ Tap the arrow at the top-left to open search</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero"><h1>Read less. <span>Understand more.</span></h1>'
                '<p>Search any open-access paper, get a structured summary in seconds, '
                'and interrogate it with questions grounded in the text.</p></div>', unsafe_allow_html=True)
    for i, p in enumerate(st.session_state.results):
        authors = ", ".join(a["author"]["display_name"] for a in p.get("authorships", [])[:3]) or "Unknown authors"
        st.markdown(f'<div class="card"><div class="t">{p.get("title","Untitled")}</div>'
                    f'<div class="m"><span class="pill">{p.get("publication_year","N/A")}</span>'
                    f'{authors} · {p.get("cited_by_count",0)} citations</div></div>', unsafe_allow_html=True)
        if st.button("Open this paper →", key=f"open{i}"):
            load_paper(p)
            if st.session_state.paper:
                st.rerun()
else:
    authors = ", ".join(a["author"]["display_name"] for a in paper.get("authorships", [])[:4]) or "Unknown authors"
    st.markdown(f'<div class="paperbar"><div class="t">{paper.get("title")}</div>'
                f'<div class="m" style="color:var(--muted);font-size:.85rem;margin-top:.3rem">'
                f'{authors} · {paper.get("publication_year","N/A")}</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    for col, val, lab in [(c1, st.session_state.chunks, "Passages indexed"),
                          (c2, paper.get("cited_by_count", 0), "Citations"),
                          (c3, len(st.session_state.messages) // 2, "Questions asked")]:
        col.markdown(f'<div class="stat"><b>{val}</b><span>{lab}</span></div>', unsafe_allow_html=True)
    st.write("")

    tab_sum, tab_chat = st.tabs(["Summary", "Ask the paper"])

    with tab_sum:
        st.markdown(clean_md(st.session_state.summary) if st.session_state.summary else "_No summary yet._")

    with tab_chat:
        if not st.session_state.messages:
            st.caption("Try one of these:")
            sugg = ["What problem does this paper solve?", "Explain the methodology simply",
                    "What datasets were used?", "What are the limitations?"]
            cols = st.columns(2)
            for i, s in enumerate(sugg):
                if cols[i % 2].button(s, key=f"s{i}", use_container_width=True):
                    st.session_state.pending = s
                    st.rerun()

        for m in st.session_state.messages:
            with st.chat_message(m["role"], avatar="🧑‍🔬" if m["role"] == "user" else "🤖"):
                st.markdown(m["content"])
                for src in m.get("sources", []):
                    st.markdown(f'<div class="src">{src}</div>', unsafe_allow_html=True)

        q = st.chat_input("Ask anything about this paper…") or st.session_state.pop("pending", None)
        if q:
            st.session_state.messages.append({"role": "user", "content": q})
            with st.chat_message("user", avatar="🧑‍🔬"):
                st.markdown(q)
            with st.chat_message("assistant", avatar="🤖"):
                stream, docs = ask_stream(q)
                answer = st.write_stream(stream)
                sources = [d.page_content[:260].replace("\n", " ") + "…" for d in docs[:3]]
                with st.expander("Source passages"):
                    for s in sources:
                        st.markdown(f'<div class="src">{s}</div>', unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.rerun()