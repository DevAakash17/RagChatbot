# LLM Service

A scalable and maintainable service for generating text using Large Language Models (LLMs).

## Features

- RESTful API for text generation
- Support for multiple LLM models (currently Gemini 2.0 Flash)
- Extensible architecture for adding new models
- Concurrent request handling
- Structured error handling
- Comprehensive logging

## Installation

### Prerequisites

- Python 3.13+
- pip

### Setup

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
# Create a .env file in the project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

## Usage

### Starting the service

```bash
python -m llm_service.main
```

The service will start on http://localhost:8000 by default.

### API Endpoints

#### Generate Text

```
POST /api/v1/generate
```

Request body:

```json
{
  "prompt": "Explain how AI works",
  "model": "gemini-2.0-flash",
  "options": {
    "temperature": 0.7,
    "max_tokens": 1024,
    "top_p": 0.95,
    "top_k": 40
  }
}
```

Response:

```json
{
  "text": "AI, or artificial intelligence, works by...",
  "model": "gemini-2.0-flash",
  "usage": {
    "prompt_tokens": 4,
    "completion_tokens": 150,
    "total_tokens": 154
  },
  "finish_reason": "STOP"
}
```

### Health Check

```
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

## Adding New Models

To add a new LLM model:

1. Create a new model implementation in `llm_service/core/models/`
2. Register the model in `llm_service/core/services/llm_service.py`
3. Add model configuration in `llm_service/config/settings.py`

## License

MIT
