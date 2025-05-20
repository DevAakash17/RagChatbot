# Embedding Service

A scalable, maintainable service for generating and managing text embeddings with a focus on performance, security, and extensibility.

## Features

- Generate text embeddings using Sentence Transformers
- Store and retrieve embeddings using ChromaDB
- RESTful API with FastAPI
- Similarity search
- Batch processing
- Comprehensive error handling and logging
- Modular architecture for easy extension

## Architecture

The service follows a modular architecture with these components:

1. **API Layer** - FastAPI endpoints
2. **Service Layer** - Business logic
3. **Embedding Layer** - Abstraction for different embedding models
4. **Vector DB Layer** - Abstraction for different vector databases
5. **Logging & Error Handling** - Consistent across all components

## Installation

### Prerequisites

- Python 3.13+
- pip

### Setup

1. Clone the repository
2. Install dependencies:

```bash
cd embedding_service
pip install -r requirements.txt
```

## Usage

### Running the Service

```bash
cd embedding_service
python -m main
```

The service will be available at http://localhost:8000.

### API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

- `POST /api/v1/embeddings` - Generate embeddings for texts
- `POST /api/v1/collections/store` - Store embeddings in a collection
- `POST /api/v1/collections/query` - Query for similar embeddings
- `GET /api/v1/collections` - List all collections
- `POST /api/v1/collections/delete` - Delete a collection
- `GET /api/v1/health` - Health check

## Configuration

Configuration is managed through environment variables or a `.env` file. Key settings include:

- `EMBEDDING_MODEL` - Name of the embedding model (default: "all-MiniLM-L6-v2")
- `VECTOR_DB_TYPE` - Type of vector database (default: "chroma")
- `VECTOR_DB_PATH` - Path to store vector database data (default: "./vector_db_data")
- `BATCH_SIZE` - Batch size for processing (default: 32)
- `LOG_LEVEL` - Logging level (default: "INFO")

## Extending the Service

### Adding a New Embedding Model

1. Create a new class in the `embeddings` directory that inherits from `BaseEmbeddingModel`
2. Implement the required methods
3. Update the `_create_embedding_model` method in `EmbeddingService` to support the new model

### Adding a New Vector Database

1. Create a new class in the `vector_db` directory that inherits from `BaseVectorDB`
2. Implement the required methods
3. Update the `_create_vector_db` method in `EmbeddingService` to support the new database

## Testing

Run tests with pytest:

```bash
pytest
```

## License

MIT
