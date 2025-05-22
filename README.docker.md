# Docker Deployment for RAG Chatbot

This repository contains Docker configuration for deploying the RAG Chatbot application with all its components.

## Components

The deployment includes:

1. **Frontend**: Next.js application running on port 3000
2. **Backend Services**:
   - Embedding Service (port 8000)
   - LLM Service (port 8001)
   - Chunker Service (port 8002)
   - RAG Engine (port 8003)
3. **MongoDB**: Database for document tracking and user management (port 27017)

## Prerequisites

- Docker and Docker Compose installed on your system
- Gemini API key (for the LLM service)

## Configuration

1. Edit the `.env` file to set your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. You can also modify other settings in the `.env` file as needed.

## Running the Application

1. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

2. Access the application:
   - Frontend: http://localhost:3000
   - Embedding Service API docs: http://localhost:8000/docs
   - LLM Service API docs: http://localhost:8001/docs
   - Chunker Service API docs: http://localhost:8002/docs
   - RAG Engine API docs: http://localhost:8003/docs

3. Stop the application:
   ```bash
   docker-compose down
   ```

## Data Persistence

The following data is persisted using Docker volumes:

- MongoDB data: `mongodb_data`
- Node.js modules: `node_modules`
- Next.js build cache: `next_cache`

## Troubleshooting

If you encounter any issues:

1. Check the logs:
   ```bash
   docker-compose logs
   ```

2. For specific service logs:
   ```bash
   docker-compose logs mongodb
   docker-compose logs chatbot
   ```

3. Restart the services:
   ```bash
   docker-compose restart
   ```

4. Rebuild the containers if you make changes to the Dockerfile:
   ```bash
   docker-compose up -d --build
   ```
