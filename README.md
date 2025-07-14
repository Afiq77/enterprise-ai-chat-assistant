# Enterprise AI Chat Assistant

An AI-powered assistant designed for enterprise use, combining LLMs with structured and unstructured data sources to deliver real-time insights and support.

## Features

- Hybrid RAG pipeline with embeddings and structured DB integration
- Intent classification and dynamic query routing
- Support for cloud (OpenAI, Gemini) and local (Mistral) LLMs
- Voice input pipeline using Whisper
- Dockerized FastAPI backend and modular frontend (React/Vite)

## Tech Stack

- Python, FastAPI
- LangChain, Hugging Face Transformers
- PostgreSQL, FAISS
- Whisper, Ollama, Gemini, OpenAI
- Frontend: React + TailwindCSS + Vite

## Folder Structure

    enterprise-ai-chat-assistant/
    ├── backend/
    │ ├── main.py
    │ ├── rag_engine.py
    │ ├── vector_store.py
    │ └── ...
    ├── frontend/
    │ ├── src/
    │ └── ...
    ├── requirements.txt
    ├── README.md
    └── .env.sample


## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/enterprise-ai-chat-assistant.git
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    
## Future Improvements

- Add user feedback loop for intent correction
- Extend RAG with web document ingestion
- Analytics dashboard with query trends

# License
  This project is licensed under the MIT License.
