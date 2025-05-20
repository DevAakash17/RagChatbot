# RAG Engine

A scalable, maintainable service for Retrieval-Augmented Generation (RAG) that integrates with the embedding_service and llm_service.

## Features

- Process user queries through a complete RAG pipeline
- Retrieve relevant context from a vector database
- Generate responses using LLMs with the retrieved context
- RESTful API with FastAPI
- Comprehensive error handling and logging
- Modular architecture for easy extension
- Concurrent request handling

## Architecture

The service follows a modular architecture with these components:

1. **API Layer** - FastAPI endpoints for interacting with the RAG Engine
2. **Service Layer** - High-level services that orchestrate the RAG process
3. **Core Layer** - Core components of the RAG pipeline:
   - Query Processor - Processes and optimizes user queries
   - Context Retriever - Retrieves relevant context using embeddings
   - Prompt Builder - Builds prompts with retrieved context
   - Response Generator - Generates responses using the LLM
4. **Client Layer** - Clients for interacting with external services:
   - Embedding Client - Client for the embedding_service
   - LLM Client - Client for the llm_service
5. **Utilities** - Logging, error handling, and configuration

## Installation

### Prerequisites

- Python 3.13+
- pip
- Running instances of the embedding_service and llm_service

### Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Service

```bash
python -m chatbot.rag_engine.main
```

The service will be available at http://localhost:8002.

### API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

### API Endpoints

- `POST /api/v1/query` - Process a query through the RAG pipeline
- `POST /api/v1/store` - Store documents in the vector database
- `GET /api/v1/collections` - List all collections in the vector database
- `GET /api/v1/health` - Check the health of the service

### Example Usage

See the `examples/example_usage.py` script for a complete example of using the RAG Engine.

## Configuration

The RAG Engine can be configured using environment variables or a `.env` file. See `.env.example` for available configuration options.

Key configuration options:

- `EMBEDDING_SERVICE_URL` - URL of the embedding service
- `LLM_SERVICE_URL` - URL of the LLM service
- `MAX_CONTEXT_DOCUMENTS` - Maximum number of documents to include in context
- `SIMILARITY_THRESHOLD` - Minimum similarity score for retrieved documents
- `DEFAULT_LLM_MODEL` - Default LLM model to use
- `DEFAULT_EMBEDDING_MODEL` - Default embedding model to use

## Extending the Service

### Adding a New Feature

1. Identify the appropriate layer for your feature
2. Implement the feature in a modular way
3. Update the relevant components to use your feature
4. Add tests for your feature

### Customizing the RAG Pipeline

The RAG pipeline can be customized by modifying the following components:

- `QueryProcessor` - Customize query processing logic
- `ContextRetriever` - Customize context retrieval logic
- `PromptBuilder` - Customize prompt building logic
- `ResponseGenerator` - Customize response generation logic

## License

[MIT License](LICENSE)
