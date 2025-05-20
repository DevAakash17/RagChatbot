"""
Example usage of the Embedding Service API.
"""
import requests
import json
from typing import Dict, Any


# API base URL
BASE_URL = "http://localhost:8000/api/v1"


def print_json(data: Dict[str, Any]):
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def generate_embeddings():
    """Generate embeddings for texts."""
    print("\n=== Generating Embeddings ===")
    
    # Request data
    data = {
        "texts": [
            "This is a sample sentence.",
            "Another example text for embedding."
        ]
    }
    
    # Make request
    response = requests.post(f"{BASE_URL}/embeddings", json=data)
    
    # Print response
    if response.status_code == 200:
        result = response.json()
        print(f"Generated {len(result['embeddings'])} embeddings using model: {result['model']}")
        print(f"Embedding dimension: {result['dimension']}")
        print(f"First embedding (truncated): {result['embeddings'][0][:5]}...")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def store_embeddings():
    """Store embeddings in a collection."""
    print("\n=== Storing Embeddings ===")
    
    # Request data
    data = {
        "texts": [
            "Artificial intelligence is transforming industries.",
            "Machine learning models can recognize patterns in data.",
            "Natural language processing helps computers understand human language.",
            "Deep learning is a subset of machine learning.",
            "Neural networks are inspired by the human brain."
        ],
        "collection_name": "ai_concepts",
        "metadata": [
            {"category": "general", "importance": "high"},
            {"category": "technical", "importance": "medium"},
            {"category": "nlp", "importance": "high"},
            {"category": "technical", "importance": "medium"},
            {"category": "technical", "importance": "low"}
        ]
    }
    
    # Make request
    response = requests.post(f"{BASE_URL}/collections/store", json=data)
    
    # Print response
    if response.status_code == 201:
        result = response.json()
        print(f"Stored {result['count']} embeddings in collection: {result['collection_name']}")
        print(f"IDs: {result['ids']}")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def query_similar():
    """Query for similar embeddings."""
    print("\n=== Querying Similar Embeddings ===")
    
    # Request data
    data = {
        "query_texts": [
            "How do computers understand language?",
            "Tell me about neural networks."
        ],
        "collection_name": "ai_concepts",
        "top_k": 2
    }
    
    # Make request
    response = requests.post(f"{BASE_URL}/collections/query", json=data)
    
    # Print response
    if response.status_code == 200:
        result = response.json()
        print(f"Query results from collection: {result['collection_name']}")
        
        for i, query_results in enumerate(result['results']):
            print(f"\nResults for query: '{data['query_texts'][i]}'")
            for j, item in enumerate(query_results):
                print(f"  {j+1}. Text: {item['text']}")
                print(f"     Score: {item['score']:.4f}")
                print(f"     Metadata: {item['metadata']}")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def list_collections():
    """List all collections."""
    print("\n=== Listing Collections ===")
    
    # Make request
    response = requests.get(f"{BASE_URL}/collections")
    
    # Print response
    if response.status_code == 200:
        result = response.json()
        print(f"Found {len(result['collections'])} collections:")
        
        for collection in result['collections']:
            print(f"  - {collection['name']}: {collection['count']} embeddings, dimension: {collection['dimension']}")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def delete_collection():
    """Delete a collection."""
    print("\n=== Deleting Collection ===")
    
    # Request data
    data = {
        "collection_name": "ai_concepts"
    }
    
    # Make request
    response = requests.post(f"{BASE_URL}/collections/delete", json=data)
    
    # Print response
    if response.status_code == 200:
        result = response.json()
        print(f"Deleted collection: {result['collection_name']}")
        print(f"Success: {result['success']}")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def check_health():
    """Check the health of the service."""
    print("\n=== Health Check ===")
    
    # Make request
    response = requests.get(f"{BASE_URL}/health")
    
    # Print response
    if response.status_code == 200:
        result = response.json()
        print(f"Status: {result['status']}")
        print(f"Version: {result['version']}")
        print(f"Embedding Model: {result['embedding_model']}")
        print(f"Vector DB: {result['vector_db']}")
    else:
        print(f"Error: {response.status_code}")
        print_json(response.json())


def main():
    """Run all examples."""
    print("=== Embedding Service API Examples ===")
    
    try:
        # Check health
        check_health()
        
        # Generate embeddings
        generate_embeddings()
        
        # Store embeddings
        store_embeddings()
        
        # List collections
        list_collections()
        
        # Query similar
        query_similar()
        
        # Delete collection
        delete_collection()
        
        # List collections again
        list_collections()
        
        print("\nAll examples completed successfully!")
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the Embedding Service.")
        print("Make sure the service is running at http://localhost:8000")


if __name__ == "__main__":
    main()
