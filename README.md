# RAG Chatbot with Microservices Architecture

A comprehensive Retrieval-Augmented Generation (RAG) chatbot system with a Next.js frontend and multiple FastAPI microservices, featuring document processing, vector embeddings, and user authentication.

## Overview

This project implements a complete RAG system that allows users to query information from processed documents. The system processes documents into chunks, embeds them into vector space, and retrieves relevant context to generate accurate responses using LLM technology.

## Architecture

The system is built on a microservices architecture with the following components:

- **Frontend**: Next.js application with authentication and chat interface
- **Authentication Service**: Handles user management and JWT authentication
- **Chunker Service**: Processes documents into semantic chunks for better retrieval
- **Embedding Service**: Converts text chunks into vector embeddings
- **Vector Database**: Stores and enables semantic search of document embeddings
- **LLM Service**: Interfaces with Gemini API for response generation
- **RAG Engine**: Orchestrates the retrieval and generation process

## Features

- **User Management**
  - User authentication (login/register)
  - Secure password storage with bcrypt encryption
  - JWT-based authentication

- **Document Processing**
  - Semantic chunking of documents
  - Support for multiple file types (PDF, DOCX, TXT)
  - Document metadata tracking

- **Chat Interface**
  - Markdown rendering for rich responses
  - Auto-scrolling to the latest message
  - Loading indicators
  - Error handling
  - Reset chat functionality
  - Typing animation for bot responses

- **RAG Capabilities**
  - Semantic search for relevant context
  - Context-aware responses
  - Citation of source documents

## Tech Stack

### Frontend
- Next.js (React + TypeScript)
- Tailwind CSS
- ShadCN UI components
- Axios for API requests
- React Markdown

### Backend
- FastAPI (Python)
- MongoDB (document storage)
- ChromaDB (vector database)
- Sentence Transformers (embeddings)
- Gemini API (LLM)
- JWT for authentication

### Infrastructure
- Docker and Docker Compose
- MongoDB for data persistence

## Prerequisites

- Node.js 16.8 or later
- Python 3.8+
- MongoDB
- Docker and Docker Compose (for containerized setup)
- Gemini API key
- npm or yarn

## Installation and Setup

### Docker Setup (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd chatbot
   ```

2. Add your Gemini API key to the `docker-compose.yml` file:
   ```yaml
   environment:
     - GEMINI_API_KEY=your_api_key_here
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Import sample data (optional):
   ```bash
   ./import_mongo_docker.sh
   ```

5. Access the application at http://localhost:3000

### Local Development Setup

#### Backend Services

1. Set up virtual environments and install dependencies for each service:

   ```bash
   # Authentication Service
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Chunker Service
   cd ../chunker_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Embedding Service
   cd ../embedding_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # LLM Service
   cd ../llm_service
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # RAG Engine
   cd ../rag_engine
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure MongoDB:
   - Make sure MongoDB is running
   - Update the `.env` files in each service directory if needed

3. Start each service:
   ```bash
   # In separate terminals
   cd backend && python main.py  # Runs on port 8005
   cd chunker_service && python main.py  # Runs on port 8002
   cd embedding_service && python main.py  # Runs on port 8000
   cd llm_service && python main.py  # Runs on port 8001
   cd rag_engine && python main.py  # Runs on port 8003
   ```

#### Frontend Setup

1. Navigate to the project root directory

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   ```

3. Run the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Data Import

The system requires MongoDB data for users and processed documents. You can import sample data using one of the provided scripts:

### For Local MongoDB

```bash
./import_mongo_data.sh
```

### For Docker MongoDB

```bash
./import_mongo_docker.sh
```

Alternatively, you can use the Python script:

```bash
python import_mongo_data.py
```

The import scripts will populate:
- `users` collection with sample user accounts
- `processed_documents` collection with document metadata and chunk references

## API Documentation

### Authentication Service (Port 8005)
- `POST /auth/login`: Authenticate a user
- `POST /auth/register`: Register a new user
- `GET /auth/me`: Get current user information

### Chunker Service (Port 8002)
- `POST /api/process`: Process a document into chunks
- `GET /api/documents`: List processed documents
- `GET /api/documents/{document_id}`: Get document details

### Embedding Service (Port 8000)
- `POST /api/embed`: Generate embeddings for text
- `POST /api/search`: Search for similar documents

### LLM Service (Port 8001)
- `POST /api/generate`: Generate text using LLM

### RAG Engine (Port 8003)
- `POST /api/v1/query`: Send a query to the RAG engine

## Project Structure

- `src/`: Frontend code
  - `app/`: Next.js app router pages
  - `components/`: React components
  - `lib/`: Utility functions, API service, and types
- `backend/`: Authentication service
- `chunker_service/`: Document processing service
- `embedding_service/`: Vector embedding service
- `llm_service/`: LLM integration service
- `rag_engine/`: RAG orchestration service
- `xtra/`: Sample data for import
- `docker-compose.yml`: Docker configuration
- `import_mongo_*.sh`: Data import scripts

## License

MIT
