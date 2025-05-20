"""
Example script to demonstrate usage of the RAG Engine.
"""
import asyncio
import json
import os
import sys

import aiohttp


async def query_rag_engine():
    """Example of using the RAG Engine API."""
    url = "http://localhost:8002/api/v1/query"

    payload = {
        "query": "What is the capital of France?",
        "collection_name": "documents",
        "top_k": 3,
        "llm_options": {
            "temperature": 0.7,
            "max_tokens": 500
        }
    }

    print(f"Sending query: {payload['query']}")
    print("Waiting for response...")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                print(await response.text())
                return

            result = await response.json()
            
            print("\nResponse:")
            print(f"Text: {result['text']}")
            print(f"Model: {result['model']}")
            print(f"Token usage: {result['usage']}")
            
            print("\nContext documents:")
            for i, doc in enumerate(result["context_documents"]):
                print(f"\nDocument {i+1}:")
                print(f"ID: {doc['id']}")
                print(f"Score: {doc['score']:.4f}")
                print(f"Text: {doc['text'][:100]}...")
                if doc.get("metadata"):
                    print(f"Metadata: {doc['metadata']}")


async def store_documents():
    """Example of storing documents in the RAG Engine."""
    url = "http://localhost:8002/api/v1/store"

    # Sample documents about world capitals
    documents = [
        "Paris is the capital and most populous city of France. It is located on the Seine River, in the north of the country.",
        "London is the capital and largest city of England and the United Kingdom. It stands on the River Thames in the south-east of England.",
        "Berlin is the capital and largest city of Germany. It is located in the northeastern part of the country.",
        "Rome is the capital city of Italy. It is located in the central-western portion of the Italian Peninsula, on the Tiber River.",
        "Madrid is the capital and most populous city of Spain. It is located on the Manzanares River in the center of the country."
    ]

    # Sample metadata for each document
    metadata = [
        {"country": "France", "continent": "Europe", "population": "2.2 million"},
        {"country": "United Kingdom", "continent": "Europe", "population": "8.9 million"},
        {"country": "Germany", "continent": "Europe", "population": "3.7 million"},
        {"country": "Italy", "continent": "Europe", "population": "2.8 million"},
        {"country": "Spain", "continent": "Europe", "population": "3.3 million"}
    ]

    payload = {
        "texts": documents,
        "collection_name": "documents",
        "metadata": metadata
    }

    print(f"Storing {len(documents)} documents...")

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                print(await response.text())
                return

            result = await response.json()
            
            print("\nDocuments stored successfully:")
            print(f"Collection: {result['collection_name']}")
            print(f"Count: {result['count']}")
            print(f"IDs: {result['ids']}")


async def list_collections():
    """Example of listing collections in the RAG Engine."""
    url = "http://localhost:8002/api/v1/collections"

    print("Listing collections...")

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error: {response.status}")
                print(await response.text())
                return

            result = await response.json()
            
            print("\nCollections:")
            for collection in result["collections"]:
                print(f"Name: {collection['name']}")
                print(f"Count: {collection['count']}")
                print(f"Dimension: {collection['dimension']}")
                print()


async def main():
    """Run the examples."""
    print("RAG Engine Example Usage")
    print("=======================")
    
    # First, store some documents
    print("\n1. Storing documents")
    print("-------------------")
    await store_documents()
    
    # List collections
    print("\n2. Listing collections")
    print("--------------------")
    await list_collections()
    
    # Query the RAG Engine
    print("\n3. Querying the RAG Engine")
    print("------------------------")
    await query_rag_engine()


if __name__ == "__main__":
    asyncio.run(main())
