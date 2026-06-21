from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import requests
import time
import os
from langchain_groq import ChatGroq
# ==============================
# Load environment variables
# ==============================
load_dotenv()

# ==============================
# Load LLM
# ==============================
model=ChatGroq(
    model_name="llama-3.3-70b-versatile",
    temperature=0
)
# ==============================
# Safe arXiv loader (handles 429)
# ==============================
from langchain_community.document_loaders import ArxivLoader

def safe_arxiv_load(query, retries=3):
    for i in range(retries):
        try:
            loader = ArxivLoader(query=query, load_max_docs=1)
            return loader.load()
        except Exception as e:
            print(f"[Retry {i+1}] arXiv error:", e)
            time.sleep(3)
    return []

# ==============================
# User input
# ==============================
user_query_paper = input("Enter the name of the paper or keywords: ").strip()

if len(user_query_paper) < 3:
    print("Please enter a more specific query.")
    exit()

print(f"\n[INFO] Searching for: {user_query_paper}")

# ==============================
# OpenAlex Search
# ==============================
OPENALEX_URL = "https://api.openalex.org/works"

params = {
    "search": f'"{user_query_paper}"',
    "filter": "is_oa:true",
    "per-page": 5
}

try:
    response = requests.get(OPENALEX_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json().get("results", [])
except Exception as e:
    print("Error fetching papers:", e)
    data = []

documents = []

# ==============================
# Process results
# ==============================
if not data:
    print("No relevant paper found. Try exact title.")
    exit()

print("\nFound Top papers:\n")

for i, paper in enumerate(data):
    title = paper.get("title", "No title")
    year = paper.get("publication_year", "N/A")
    print(f"{i+1}. {title} ({year})")

# ==============================
# Safe user choice
# ==============================
try:
    choice = int(input("Enter your choice (1-5): ")) - 1
    if choice < 0 or choice >= len(data):
        raise ValueError
except:
    print("Invalid choice. Selecting first paper.")
    choice = 0

selected_paper = data[choice]
selected_title = selected_paper.get("title", "")

print(f"\nUsing paper: {selected_title}")

# ==============================
# Relevance warning
# ==============================
if user_query_paper.lower() not in selected_title.lower():
    print("⚠️ Warning: This may not be the exact paper")

# ==============================
# Extract arXiv ID
# ==============================
def get_arxiv_id(paper):
    locations = paper.get("locations", [])
    
    for loc in locations:
        url = loc.get("landing_page_url") or ""
        if "arxiv.org" in url:
            return url.split("/")[-1]
    
    return None

arxiv_id = get_arxiv_id(selected_paper)

# ==============================
# Load paper
# ==============================
if arxiv_id:
    documents = safe_arxiv_load(arxiv_id)
else:
    print("No arXiv ID found. Trying direct search...")
    documents = safe_arxiv_load(user_query_paper)

# ==============================
# Final fallback
# ==============================
if not documents:
    print("Failed to load paper. Please try another query.")
    exit()

# ==============================
# Chunking
# ==============================
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

# ==============================
# Embeddings
# ==============================
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2'
)

# ==============================
# Vector Store
# ==============================
from langchain_community.vectorstores import FAISS

vector_db = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

retriever = vector_db.as_retriever(
    search_type='mmr',
    search_kwargs={"k": 5}
)

# ==============================
# Prompt
# ==============================
prompt = ChatPromptTemplate.from_template("""
You are RABOT, a research paper assistant.

Instructions:
1. Answer only using the provided paper context.
2. If the answer is unavailable, say:
   "This information is not available in the paper."
3. Be factual and concise.
4. Use bullet points when appropriate.
5. For summaries provide:
   - Problem
   - Methodology
   - Key Contributions
   - Results
   - Limitations

Context:
{context}

Question:
{Question}

Answer:

""")

# ==============================
# Parser
# ==============================
parser = StrOutputParser()

# ==============================
# RAG Chain
# ==============================
rag_chain = (
    {
        "context": retriever,
        "Question": RunnablePassthrough()
    }
    | prompt
    | model
    | parser
)

# ==============================
# Invoke
# ==============================
result = rag_chain.invoke("Give a structured summary of the paper.")
print("\n=== RESULT ===\n")
print(result)
