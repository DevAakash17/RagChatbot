#!/bin/bash
set -e

echo "Starting RAG Chatbot Application..."

# Create necessary directories
mkdir -p /app/vector_db_data
mkdir -p /app/storage_data

# Start backend services in the background
echo "Starting Embedding Service..."
cd /chatbot && python -m uvicorn embedding_service.main:app --host 0.0.0.0 --port 8000 --reload &

echo "Starting LLM Service..."
cd /chatbot && python -m uvicorn llm_service.main:app --host 0.0.0.0 --port 8001 --reload &

echo "Starting Chunker Service..."
cd /chatbot && python -m uvicorn chunker_service.main:app --host 0.0.0.0 --port 8002 --reload &

echo "Starting RAG Engine..."
cd /chatbot && python -m uvicorn rag_engine.main:app --host 0.0.0.0 --port 8003 --reload &

# Wait for backend services to start
echo "Waiting for backend services to start..."
sleep 10

# Start the frontend
echo "Starting Frontend..."
npm run start

# Keep the container running
exec "$@"
