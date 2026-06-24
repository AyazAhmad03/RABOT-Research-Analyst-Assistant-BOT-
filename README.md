# 📚 RABOT: AI-Powered Research Paper Assistant

## Overview

RABOT (Research Assistant Bot) is an AI-powered research companion that helps users discover, understand, summarize, and interact with academic research papers through natural language conversations.

Built using Retrieval-Augmented Generation (RAG), RABOT combines paper discovery, document retrieval, semantic search, vector databases, and Large Language Models to provide context-aware answers grounded in research papers.

Users can search for papers, load full-text research articles, generate structured summaries, and ask unlimited questions about the paper's content.

---

## Features

### 🔍 Intelligent Paper Discovery

* Search research papers using OpenAlex.
* Retrieve the most relevant papers based on keywords or titles.
* Display multiple candidate papers for user selection.

### 📄 Automated Research Paper Retrieval

* Load papers directly from arXiv.
* Automatic extraction and processing of research paper content.
* Retry mechanism for robust document loading.

### 🧠 AI-Powered Paper Summarization

Generate structured summaries including:

* Research Problem
* Methodology
* Key Contributions
* Results
* Limitations

### 💬 Conversational Research Assistant

* Ask unlimited questions about the selected paper.
* Context-aware responses grounded in the document.
* Hallucination reduction using Retrieval-Augmented Generation.

### ⚡ Retrieval-Augmented Generation (RAG)

* Semantic chunking of research papers.
* Vector embeddings using Sentence Transformers.
* Persistent vector storage using ChromaDB.
* Context retrieval for accurate paper understanding.
* Groq-powered LLM inference.

### 💾 Persistent Knowledge Base

* Embeddings are stored locally using ChromaDB.
* Previously processed papers can be loaded instantly.
* Avoids recomputing embeddings for the same paper.

### 🚀 Modern Web Interface

* Streamlit-based UI.
* Interactive landing page.
* Paper search, loading, summarization, and Q&A in one application.

---

## System Architecture

```text
User Query
     │
     ▼
OpenAlex Search
     │
     ▼
Paper Selection
     │
     ▼
arXiv Retrieval
     │
     ▼
Document Chunking
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB Vector Store
     │
     ▼
Retriever
     │
     ▼
Groq Llama 3.3 70B
     │
     ▼
Final Response
```

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python
* LangChain

### AI & Machine Learning

* Groq API
* Llama 3.3 70B Versatile
* Sentence Transformers
* Retrieval-Augmented Generation (RAG)

### Vector Database

* ChromaDB

### Research Sources

* OpenAlex API
* arXiv API

### Supporting Libraries

* LangChain
* LangChain Chroma
* LangChain Community
* LangChain Groq
* Requests
* Python Dotenv

---

## Installation

### Clone Repository

```bash
git clone https://github.com/AyazAhmad03/rabot.git
cd rabot
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
```

### Run Application

```bash
streamlit run app.py
```

---

## Example Questions

### Paper Understanding

* Give a structured summary of the paper.
* Explain the paper in detail.
* What problem does this paper solve?
* What are the key contributions?

### Technical Analysis

* Explain the methodology.
* Explain the mathematical formulation.
* What datasets were used?
* How does this compare with previous approaches?

### Research Insights

* What are the limitations?
* What future work is suggested?
* What are the main experimental results?

---

## Future Enhancements

* PDF Upload Support
* Multi-Paper Comparison
* Research Paper Recommendation Engine
* Citation-Aware Responses
* Conversational Memory
* Export Summaries to PDF
* Source Chunk Visualization
* Multi-Agent Research Workflow

---

## Project Highlights

* End-to-End Retrieval-Augmented Generation Pipeline
* Research Paper Search and Retrieval
* Persistent ChromaDB Knowledge Base
* Semantic Search over Research Papers
* Groq-Powered Large Language Models
* Context-Grounded Question Answering
* Research-Focused AI Assistant

---

## Author

**Ayaz Ahmad**

GitHub:
https://github.com/AyazAhmad03

---

## License

This project is intended for educational, research, and portfolio purposes.

Responses are generated using AI and retrieved paper content.

Users should verify important findings directly from the original research paper.
