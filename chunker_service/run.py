"""
Script to run the Chunker Service.
"""
import uvicorn
import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    """Run the application."""
    uvicorn.run(
        "chatbot.chunker_service.main:app",
        host="0.0.0.0",
        port=8002,  # Use a different port than embedding_service and llm_service
        reload=True,
        log_level="info"
    )
