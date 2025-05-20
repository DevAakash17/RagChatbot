# Chunker Service

A scalable, maintainable service for chunking documents and storing embeddings in a vector database.

## Features

- Read data from object storage in a streaming manner
- Chunk data into smaller pieces using configurable strategies
- Update the vector database using the embedding service
- Document tracking to avoid reprocessing already processed documents
- RESTful API with FastAPI
- Support for multiple storage providers (local filesystem, S3)
- Support for multiple chunking strategies (fixed size, semantic)
- Support for multiple document formats (text, PDF, DOCX)
- Comprehensive error handling and logging
- Concurrent request handling
- Modular architecture for easy extension

## Architecture

The service follows a modular architecture with these components:

1. **API Layer** - FastAPI endpoints for chunking operations
2. **Service Layer** - Core chunking business logic
3. **Storage Layer** - Abstraction for different object storage providers
4. **Chunking Layer** - Different chunking strategies
5. **Client Layer** - Client for interacting with the embedding service
6. **Database Layer** - MongoDB integration for document tracking
7. **Utilities** - Logging, error handling, and configuration

## Installation

### Prerequisites

- Python 3.13+
- pip
- MongoDB (for document tracking)

### Setup

1. Clone the repository
2. Install dependencies:

```bash
cd chunker_service
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
# Create a .env file in the project root
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Service

```bash
cd chunker_service
python run.py
```

The service will be available at http://localhost:8002.

### API Documentation

Once the service is running, you can access the API documentation at:

- Swagger UI: http://localhost:8002/docs
- ReDoc: http://localhost:8002/redoc

### API Endpoints

#### Chunk Document

```
POST /api/v1/chunk
```

Request body:

```json
{
  "document_path": "documents/sample.pdf",
  "collection_name": "my_documents",
  "chunking_strategy": "fixed_size",
  "chunking_params": {
    "chunk_size": 1000,
    "chunk_overlap": 200
  },
  "embedding_model": "all-MiniLM-L6-v2",
  "storage_type": "local",
  "document_metadata": {
    "source": "example",
    "author": "John Doe"
  }
}
```

#### Chunk Collection

```
POST /api/v1/chunk/collection
```

Request body:

```json
{
  "collection_path": "documents/",
  "vector_collection_name": "my_documents",
  "chunking_strategy": "semantic",
  "file_extensions": [".pdf", ".txt", ".docx"],
  "collection_metadata": {
    "source": "example",
    "category": "documentation"
  }
}
```

#### List Collections

```
GET /api/v1/collections
```

#### Health Check

```
GET /api/v1/health
```

## Configuration

The service can be configured through environment variables:

- `API_V1_STR` - API prefix (default: "/api/v1")
- `PROJECT_NAME` - Project name (default: "Chunker Service")
- `EMBEDDING_SERVICE_URL` - URL of the embedding service (default: "http://localhost:8000/api/v1")
- `STORAGE_TYPE` - Type of storage (default: "local")
- `STORAGE_BASE_PATH` - Base path for local storage (default: "./storage_data")
- `S3_ENDPOINT` - S3 endpoint URL (for S3 storage)
- `S3_ACCESS_KEY` - S3 access key (for S3 storage)
- `S3_SECRET_KEY` - S3 secret key (for S3 storage)
- `S3_REGION` - S3 region (for S3 storage)
- `DEFAULT_CHUNK_SIZE` - Default chunk size (default: 1000)
- `DEFAULT_CHUNK_OVERLAP` - Default chunk overlap (default: 200)
- `DEFAULT_CHUNKING_STRATEGY` - Default chunking strategy (default: "fixed_size")
- `DEFAULT_EMBEDDING_MODEL` - Default embedding model (default: "all-MiniLM-L6-v2")
- `DEFAULT_COLLECTION_NAME` - Default collection name (default: "documents")
- `BATCH_SIZE` - Batch size for processing (default: 32)
- `MAX_CONCURRENT_REQUESTS` - Maximum concurrent requests (default: 10)
- `TIMEOUT` - Timeout for requests (default: 60)
- `LOG_LEVEL` - Logging level (default: "INFO")
- `LOG_FILE` - Log file (default: "chunker_service.log")
- `MONGODB_CONNECTION_STRING` - MongoDB connection string (default: "mongodb://localhost:27017")
- `MONGODB_DATABASE_NAME` - MongoDB database name (default: "chunker_service")
- `MONGODB_DOCUMENT_COLLECTION` - MongoDB collection for document tracking (default: "processed_documents")

## Extending the Service

### Adding a New Storage Provider

1. Create a new class in the `storage` directory that inherits from `BaseStorageAdapter`
2. Implement the required methods
3. Update the `get_storage_adapter` function in `storage/__init__.py` to support the new provider

### Adding a New Chunking Strategy

1. Create a new class in the `chunking` directory that inherits from `BaseChunkingStrategy`
2. Implement the required methods
3. Update the `get_chunking_strategy` function in `chunking/__init__.py` to support the new strategy

### Document Tracking

The service uses MongoDB to track processed documents, which enables:

1. **Deduplication**: Avoids reprocessing documents that have already been chunked and embedded
2. **Versioning**: Tracks document changes using content hashing
3. **Metadata Storage**: Maintains metadata about processed documents
4. **Efficiency**: Saves computational resources by skipping already processed files

## License

MIT
