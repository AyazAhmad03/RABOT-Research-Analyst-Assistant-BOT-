import streamlit as st
import requests
import time
import os

from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace,
    HuggingFaceEmbeddings
)
from langchain_groq import ChatGroq

from langchain_community.document_loaders import ArxivLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="RABOT",
    page_icon="📚",
    layout="wide"
)


# ==========================================
# LLM
# ==========================================
@st.cache_resource
def load_llm():

    model = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0
    )

    return model

model = load_llm()


@st.cache_resource
def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

# ==========================================
# ARXIV SAFE LOADER
# ==========================================

def safe_arxiv_load(query, retries=3):

    for i in range(retries):

        try:
            loader = ArxivLoader(
                query=query,
                load_max_docs=1
            )

            return loader.load()
        except Exception as e:
            st.error(
        f"Retry {i+1}: {str(e)}"
        )
            print(
                f"ARXIV ERROR: {e}"
                  )
            time.sleep(2)

    return []

# ==========================================
# OPENALEX SEARCH
# ==========================================

def search_papers(query):

    url = "https://api.openalex.org/works"

    params = {
        "search": query,
        "filter": "is_oa:true",
        "per-page": 5
    }
    
    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        return response.json().get(
            "results",
            []
        )
    except Exception as e:
        st.error(str(e))

    return []

# ==========================================
# GET ARXIV ID
# ==========================================

def get_arxiv_id(paper):

    locations = paper.get(
        "locations",
        []
    )

    for loc in locations:

        url = loc.get(
            "landing_page_url"
        )

        if url and "arxiv.org" in url:

            return url.split("/")[-1]

    return None

# ==========================================
# BUILD RAG
# ==========================================

def build_rag_chain(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(
        documents
    )

    embeddings = get_embeddings()

    vector_db = FAISS.from_documents(
        chunks,
        embeddings
    )

    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 5}
    )

    prompt = ChatPromptTemplate.from_template(
        """
You are RABOT, a research paper assistant.

Rules:
- Answer ONLY from provided context.
- If answer not available, say:
  "Not found in the paper."
- Do not hallucinate.
- Be concise and factual.

Context:
{context}

Question:
{Question}

Answer:
"""
    )

    parser = StrOutputParser()

    rag_chain = (
        {
            "context": retriever,
            "Question": RunnablePassthrough()
        }
        | prompt
        | model
        | parser
    )

    return rag_chain

# ==========================================
# UI
# ==========================================

st.title("📚 RABOT")
st.subheader(
    "Research Paper Assistant"
)

# ==========================================
# SEARCH PAPER
# ==========================================

query = st.text_input(
    "Enter Paper Title or Keywords"
)

if st.button("Search Papers"):

    if query.strip() == "":
        st.warning(
            "Enter a paper title."
        )

    else:

        with st.spinner(
            "Searching papers..."
        ):

            papers = search_papers(query)

            st.session_state.papers = papers

# ==========================================
# SHOW RESULTS
# ==========================================

if "papers" in st.session_state:

    papers = st.session_state.papers

    if len(papers) == 0:

        st.error(
            "No papers found."
        )

    else:

        titles = [
            p["title"]
            for p in papers
        ]

        selected_title = st.radio(
            "Select a Paper",
            titles
        )

        if st.button(
            "Load Selected Paper"
        ):

            selected_paper = next(
                p for p in papers
                if p["title"] == selected_title
            )

            arxiv_id = get_arxiv_id(
                selected_paper
            )

            with st.spinner(
                "Loading paper..."
            ):

                if arxiv_id:

                    docs = safe_arxiv_load(
                        arxiv_id
                    )

                else:

                    docs = safe_arxiv_load(
                        selected_title
                    )

            if not docs:

                st.error(
                    "Unable to load paper."
                )

            else:

                with st.spinner(
                    "Creating vector database..."
                ):

                    rag_chain = build_rag_chain(
                        docs
                    )

                st.session_state.rag_chain = (
                    rag_chain
                )

                st.session_state.paper_title = (
                    selected_title
                )

                st.success(
                    "Paper loaded successfully!"
                )

# ==========================================
# PAPER READY
# ==========================================

if "rag_chain" in st.session_state:

    st.divider()

    st.success(
        f"Loaded Paper: {st.session_state.paper_title}"
    )

    # ======================================
    # AUTO SUMMARY
    # ======================================

    if st.button(
        "Generate Paper Summary"
    ):

        with st.spinner(
            "Generating summary..."
        ):

            summary = (
                st.session_state.rag_chain.invoke(
                    "Give a structured summary of this paper."
                )
            )

        st.markdown(summary)

    # ======================================
    # ASK QUESTION
    # ======================================

    question = st.text_input(
        "Ask any question about the paper"
    )

    if st.button("Ask"):

        if question.strip():

            with st.spinner(
                "Thinking..."
            ):

                answer = (
                    st.session_state.rag_chain.invoke(
                        question
                    )
                )

            st.markdown("### Answer")

            st.write(answer)