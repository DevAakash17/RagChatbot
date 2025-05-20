"""
Tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from ..main import app


# Create test client
client = TestClient(app)


def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health():
    """Test the health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_generate_embeddings():
    """Test generating embeddings."""
    request_data = {
        "texts": ["This is a test sentence."]
    }
    response = client.post("/api/v1/embeddings", json=request_data)
    assert response.status_code == 200
    assert "embeddings" in response.json()
    assert "model" in response.json()
    assert "dimension" in response.json()
    assert len(response.json()["embeddings"]) == 1


def test_store_and_query():
    """Test storing and querying embeddings."""
    # Store embeddings
    store_data = {
        "texts": ["This is a test sentence for storage."],
        "collection_name": "test_collection",
        "metadata": [{"source": "test"}]
    }
    store_response = client.post("/api/v1/collections/store", json=store_data)
    assert store_response.status_code == 201
    assert store_response.json()["collection_name"] == "test_collection"
    assert store_response.json()["count"] == 1
    
    # Query embeddings
    query_data = {
        "query_texts": ["This is a similar test sentence."],
        "collection_name": "test_collection",
        "top_k": 1
    }
    query_response = client.post("/api/v1/collections/query", json=query_data)
    assert query_response.status_code == 200
    assert query_response.json()["collection_name"] == "test_collection"
    assert len(query_response.json()["results"]) == 1
    assert len(query_response.json()["results"][0]) == 1


def test_list_collections():
    """Test listing collections."""
    response = client.get("/api/v1/collections")
    assert response.status_code == 200
    assert "collections" in response.json()
    
    # Check if test_collection exists
    collections = response.json()["collections"]
    test_collection = next((c for c in collections if c["name"] == "test_collection"), None)
    assert test_collection is not None


def test_delete_collection():
    """Test deleting a collection."""
    delete_data = {
        "collection_name": "test_collection"
    }
    response = client.post("/api/v1/collections/delete", json=delete_data)
    assert response.status_code == 200
    assert response.json()["collection_name"] == "test_collection"
    assert response.json()["success"] is True
