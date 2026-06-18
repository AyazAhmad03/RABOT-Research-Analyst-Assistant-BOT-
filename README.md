# 📚 RABOT: Research Assistant Bot

## Overview

RABOT is an AI-powered Research Assistant that enables users to discover, summarize, and interact with research papers through natural language conversations. Built using Retrieval-Augmented Generation (RAG), the system combines academic paper retrieval with Large Language Models (LLMs) to provide context-aware and accurate responses grounded in the selected research paper.

The application allows users to search for papers using keywords or titles, retrieve relevant publications from OpenAlex, load full-text papers from arXiv, generate structured summaries, and ask unlimited questions about the paper's content.

---

## Key Features

### 🔍 Intelligent Paper Discovery

* Search research papers using OpenAlex.
* Retrieve top matching papers based on user queries.
* Display multiple candidate papers for selection.

### 📄 Automated Paper Retrieval

* Fetch research papers directly from arXiv.
* Automatic extraction and processing of paper content.
* Retry mechanism for robust document loading.

### 🧠 AI-Powered Summarization

* Generate structured summaries including:

  * Research Problem
  * Methodology
  * Key Contributions
  * Results
  * Limitations

### 💬 Conversational Research Assistant

* Ask unlimited questions related to the selected paper.
* Context-aware responses grounded in the document.
* Hallucination-reduction through retrieval-based generation.

### ⚡ Retrieval-Augmented Generation (RAG)

* Semantic chunking of research papers.
* Vector embeddings using Sentence Transformers.
* FAISS-powered similarity search and retrieval.
* Context injection into LLM prompts for accurate responses.

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
 arXiv Paper Retrieval
     │
     ▼
 Text Chunking
     │
     ▼
 Embedding Generation
     │
     ▼
 FAISS Vector Store
     │
     ▼
 Context Retrieval
     │
     ▼
 Llama 3.1 (RAG)
     │
     ▼
 Final Answer
```

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python
* LangChain

### AI & Machine Learning

* Llama 3.1 8B Instruct
* Hugging Face Inference API
* Sentence Transformers

### Vector Database

* FAISS

### Data Sources

* OpenAlex API
* arXiv API

### Supporting Libraries

* LangChain Community
* LangChain HuggingFace
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
HUGGINGFACEHUB_API_TOKEN=YOUR_HUGGINGFACE_TOKEN
```

### Run Application

```bash
streamlit run app.py
```

---

## Example Questions

* Give a structured summary of the paper.
* What problem does this paper solve?
* Explain the proposed methodology.
* What datasets were used in the experiments?
* What are the key contributions of the paper?
* What are the limitations discussed by the authors?
* Compare the proposed approach with previous methods.

---

## Future Enhancements

* Multi-turn conversational memory
* PDF upload support for non-arXiv papers
* Citation-aware responses
* Multi-paper comparison
* Research paper recommendation engine
* Export summaries to PDF
* Source chunk visualization

---

## Project Highlights

* End-to-end Retrieval-Augmented Generation pipeline.
* Academic paper search and retrieval integration.
* Semantic document understanding using vector embeddings.
* Context-grounded question answering system.
* Scalable architecture suitable for research and educational use.

---

## Author

**Ayaz Ahmad**
B.Tech (Artificial Intelligence & Machine Learning)
Delhi Technical Campus, GGSIPU

GitHub: https://github.com/AyazAhmad03

---

## License

This project is intended for educational, research, and portfolio purposes.
