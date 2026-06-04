# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser

# ## load environment variables..

# load_dotenv()

# # loading Mdoel..

# llm=HuggingFaceEndpoint(
#     repo_id="meta-llama/Llama-3.1-8B-Instruct",
#     provider="novita"
# )
# model=ChatHuggingFace(llm=llm)

# # user enters paper name or keywords..

# user_query_paper=input("Enter the name of the paper in full.")

# exact_query = f'"{user_query_paper}"'   

# import requests
# SEARCH_URL= "https://api.semanticscholar.org/graph/v1/paper/search"
# params={
#     "query":exact_query,
#     "limit":5,
#     "fields":"title,year,authors,externalIds,citationCount"

# }

# response=requests.get(SEARCH_URL,params=params)
# data=response.json().get("data",[])
# documents=[]

# if not data:
#     print("No papers found .. please upload the pdf..")
# else:
#     print("\n Found Top 5 papers matching your query:\n")
#     for i,paper in enumerate(data):
#         print(f"{i+1}. {paper['title']} ({paper.get('year','N/A')})")

#     choice=int(input("Enter your choice (1-5): "))-1
#     selected_paper=data[choice]

#     print(f"\nUsing paper: {selected_paper['title']}")
#     arxiv_id = selected_paper.get("externalIds", {}).get("ArXiv")
    
#     if arxiv_id:
#         from langchain_community.document_loaders import ArxivLoader
#         documents=ArxivLoader(
#             query=arxiv_id,
#             load_max_docs=1
#             ).load()
#     else:
#         print("No arxiv_id found..upload pdf please..")


# # if paper not found in arxiv the user will upload the pdf..

# if not documents:
#     from langchain_community.document_loaders import PyPDFLoader
#     loader=PyPDFLoader("Attention is all you need.pdf")
#     documents=loader.load()

# ## splitting into chunks..

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# splitter=RecursiveCharacterTextSplitter(
#     chunk_size=200,
#     chunk_overlap=10
# )
# chunks=splitter.split_documents(documents)

# ## creating embedding vector of documents...

# from langchain_huggingface import HuggingFaceEmbeddings
# embeddings=HuggingFaceEmbeddings(
#     model_name='sentence-transformers/all-MiniLM-L6-v2'
# )

# ## storing the vector in vector store...

# from langchain_community.vectorstores import FAISS
# vector_db=FAISS.from_documents(
#     documents=chunks,
#     embedding=embeddings
# )
# retriever = vector_db.as_retriever(search_type='mmr',search_kwargs={"k": 5})

# # prompt template.....

# from langchain_core.prompts import ChatPromptTemplate
# prompt=ChatPromptTemplate.from_template("""
# You are a research assistant.
# Answer ONLY using the provided context.
# If the answer is not in the context, say "Not found in the paper".
                                
# context:
# {context}
# Question:
# {Question}
                                                                                                                    
# Answer clearly and concisely.
                                                                    
# """)

# # parser....

# parser=StrOutputParser()

# # chaining..

# from langchain_core.runnables import RunnableLambda,RunnablePassthrough
# rag_chain=(
#     { 
#     "context":retriever,
#     "Question":RunnablePassthrough()
#     }
#     | prompt
#     | model
#     | parser
# )

# # invoking and printing result..

# result=rag_chain.invoke("Give a structured summary of the paper.")
# print(result)

# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
# from dotenv import load_dotenv
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnablePassthrough
# import requests

# # ==============================
# # Load environment variables
# # ==============================
# load_dotenv()

# # ==============================
# # Load LLM
# # ==============================
# llm = HuggingFaceEndpoint(
#     repo_id="meta-llama/Llama-3.1-8B-Instruct",
#     provider="novita"
# )
# model = ChatHuggingFace(llm=llm)

# # ==============================
# # User input
# # ==============================
# user_query_paper = input("Enter the name of the paper or keywords: ")

# # ==============================
# # OpenAlex Search
# # ==============================
# OPENALEX_URL = "https://api.openalex.org/works"

# params = {
#     "search": f'"{user_query_paper}"',
#     "filter": "is_oa:true",
#     "per-page": 5
# }

# response = requests.get(OPENALEX_URL, params=params)
# data = response.json().get("results", [])

# documents = []

# if not data:
#     print("No papers found.. please upload the pdf..")

# else:
#     print("\nFound Top 5 papers matching your query:\n")

#     for i, paper in enumerate(data):
#         title = paper.get("title", "No title")
#         year = paper.get("publication_year", "N/A")
#         print(f"{i+1}. {title} ({year})")

#     choice = int(input("Enter your choice (1-5): ")) - 1
#     selected_paper = data[choice]

#     print(f"\nUsing paper: {selected_paper.get('title')}")

#     # ==============================
#     # Extract arXiv ID from OpenAlex
#     # ==============================
#     def get_arxiv_id(paper):
#         locations = paper.get("locations", [])
        
#         for loc in locations:
#             url = loc.get("landing_page_url") or ""
#             if "arxiv.org" in url:
#                 return url.split("/")[-1]
        
#         return None

#     arxiv_id = get_arxiv_id(selected_paper)

#     # ==============================
#     # Load paper using arXiv
#     # ==============================
#     if arxiv_id:
#         from langchain_community.document_loaders import ArxivLoader
        
#         documents = ArxivLoader(
#             query=arxiv_id,
#             load_max_docs=1
#         ).load()
#     else:
#         print("No arXiv ID found.. upload PDF please..")

# # ==============================
# # If no arXiv → Load PDF
# # ==============================
# if not documents:
#     from langchain_community.document_loaders import PyPDFLoader
    
#     loader = PyPDFLoader("Attention is all you need.pdf")
#     documents = loader.load()

# # ==============================
# # Chunking
# # ==============================
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=700,
#     chunk_overlap=100
# )

# chunks = splitter.split_documents(documents)

# # ==============================
# # Embeddings
# # ==============================
# from langchain_huggingface import HuggingFaceEmbeddings

# embeddings = HuggingFaceEmbeddings(
#     model_name='sentence-transformers/all-MiniLM-L6-v2'
# )

# # ==============================
# # Vector Store
# # ==============================
# from langchain_community.vectorstores import FAISS

# vector_db = FAISS.from_documents(
#     documents=chunks,
#     embedding=embeddings
# )

# retriever = vector_db.as_retriever(
#     search_type='mmr',
#     search_kwargs={"k": 5}
# )

# # ==============================
# # Prompt
# # ==============================
# prompt = ChatPromptTemplate.from_template("""
# You are a research assistant.
# Answer ONLY using the provided context.
# If the answer is not in the context, say "Not found in the paper".

# context:
# {context}

# Question:
# {Question}

# Answer clearly and concisely.
# """)

# # ==============================
# # Parser
# # ==============================
# parser = StrOutputParser()

# # ==============================
# # RAG Chain
# # ==============================
# rag_chain = (
#     {
#         "context": retriever,
#         "Question": RunnablePassthrough()
#     }
#     | prompt
#     | model
#     | parser
# )

# # ==============================
# # Invoke
# # ==============================
# result = rag_chain.invoke("Give a structured summary of the paper.")
# print(result)





from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import requests
import time

# ==============================
# Load environment variables
# ==============================
load_dotenv()

# ==============================
# Load LLM
# ==============================
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    provider="novita"
)
model = ChatHuggingFace(llm=llm)

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
You are a precise research assistant.

Rules:
- Answer ONLY from the provided context
- If not found, say: "Not found in the paper"
- Do NOT guess

Context:
{context}

Question:
{Question}

Answer clearly and concisely.
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
