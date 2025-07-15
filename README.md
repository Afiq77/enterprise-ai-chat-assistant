# Enterprise AI Chat Assistant

An end-to-end AI assistant capable of answering natural language questions about order data and live vehicle telemetry. This assistant uses Retrieval-Augmented Generation (RAG), vector embeddings, and multiple LLM backends including OpenAI, Gemini, and local models.

---

## Project Overview

The assistant includes:

- A FastAPI-based backend for data ingestion, preprocessing, vector indexing, and LLM-based query handling.
- A frontend built using React (Vite + Tailwind CSS) providing a clean chat interface.
- Integration with PostgreSQL for order data and support for external vehicle APIs.
- Modular architecture for handling multiple data types and model providers.

---

## Project Structure

        enterprise-ai-chat-assistant/
        │
        ├── app/ # Backend application logic
        │ ├── data_loader.py
        │ ├── llm_wrapper.py
        │ ├── rag_engine.py
        │ ├── vector_store.py
        │ ├── embedder.py
        │ ├── order_loader.py
        │ ├── order_vector.py
        │ ├── order_formatter.py
        │ ├── order_filter.py
        │ ├── vehicle_filter.py
        │ ├── vehicle_formatter.py
        │ ├── external_api_loader.py
        │ ├── utils.py
        │ ├── main.py
        │ └── data/ # Cached and mock data
        │ ├── orders.json
        │ ├── order_chunks.json
        │ ├── order_embeddings.npy
        │ ├── order_checksum.txt
        │ └── cached_trucks.json
        │
        ├── frontend/ # React-based chat interface
        │ └── ... # (components, styles, config files)
        │
        ├── .gitignore
        ├── .gitattributes
        ├── requirements.txt
        └── README.md



---

## Features

### Backend (FastAPI)

- Semantic search over order data using FAISS vector store.
- Structured filters for order status, material, branch, dates, etc.
- Real-time vehicle filtering (speed, region, fuel type, alarms).
- LLM integration via wrapper (OpenAI, Gemini, or local Ollama/Mistral).
- Support for audio queries and dynamic title generation.

### Frontend (React + Tailwind)

- Chat interface with real-time message streaming.
- Input handling, session memory, typing indicators.
- Clean and extensible component-based architecture.

### Module Extensibility

This project currently includes two primary modules:

- Order Intelligence (via RAG-based order data processing)
- Vehicle Intelligence (via AFAQY API live vehicle data filtering)

The system is modular by design and can be expanded to support additional enterprise modules such as:

- Contract Management
- Driver Insights
- Finance & Billing
- Customer Support
- Maintenance & Alerts
- Inventory and Logistics

Each new module can be plugged into the existing backend via its own loader, formatter, vector indexing, and query logic.

## Installation

### Backend Setup
    
    ```bash
    # Clone the repository
    git clone https://github.com/Afiq77/enterprise-ai-chat-assistant.git
    cd enterprise-ai-chat-assistant
    
    # Create a virtual environment
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    
    # Install backend dependencies
    pip install -r requirements.txt
    
    # Create .env file for PostgreSQL connection
    # .env
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=your_db_name
    DB_USER=your_username
    DB_PASSWORD=your_password
    
    # Run the FastAPI server
    uvicorn app.main:app --reload

### Frontend Setup

    cd frontend

    # Install frontend dependencies
    npm install

    # Run frontend
    npm run dev

### API Endpoints
        Method	Endpoint	            Description
        POST	/chat	            General vehicle data query
        POST	/chat_order	    Semantic and order number query
        POST	/generate_title	    Suggest a title from a message prompt
        POST	/voice-query	    Accepts audio file and responds
        POST	/refresh	    Refreshes loaded data from sources

### Data Folder (app/data/)
### These files are either auto-generated or provided as mock data to enable development without relying on a live database or API.
    File	                                        Description
    orders.json	                Enriched order records (fetched and preprocessed)
    order_chunks.json	        Flattened and chunked order text
    order_embeddings.npy	        Precomputed vector embeddings for each chunk
    order_checksum.txt	        MD5 checksum to detect changes in order data
    cached_trucks.json	        Sample truck/vehicle data from the external API

### Example Queries
- Orders created this month with quantity greater than 20
- Status of order ON40351
- Trucks currently moving in the eastern region
- Trucks with fuel type diesel and hard cornering alarms
- Vehicle 6724 LRA location and current speed

### License
This project is provided for educational and non-commercial use.

### Maintainer
Developed by Aboobakkar Siddeek Afik. For any collaboration, reach out via GitHub.
