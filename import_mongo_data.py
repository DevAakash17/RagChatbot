#!/usr/bin/env python3
"""
Script to import JSON data into MongoDB for the RAG Chatbot application.
This script imports users and processed_documents collections from JSON files.
"""

import json
import os
import sys
from pymongo import MongoClient
from bson import json_util
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_json_file(file_path):
    """Parse a JSON file and return the data."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error parsing JSON file {file_path}: {str(e)}")
        return None

def connect_to_mongodb(connection_string="mongodb://localhost:27017", db_name="chunker_service"):
    """Connect to MongoDB and return the database object."""
    try:
        client = MongoClient(connection_string)
        db = client[db_name]
        logger.info(f"Connected to MongoDB database: {db_name}")
        return db
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        return None

def import_collection(db, collection_name, data):
    """Import data into a MongoDB collection."""
    if not data:
        logger.warning(f"No data to import for collection: {collection_name}")
        return False

    try:
        # Check if collection already has data
        existing_count = db[collection_name].count_documents({})
        if existing_count > 0:
            logger.info(f"Collection {collection_name} already has {existing_count} documents. Skipping import.")
            return True

        # Convert MongoDB extended JSON format
        for item in data:
            if '_id' in item and '$oid' in item['_id']:
                item['_id'] = item['_id']['$oid']
            
            # Handle date fields
            if 'created_at' in item and '$date' in item['created_at']:
                item['created_at'] = item['created_at']['$date']

        # Insert the data
        result = db[collection_name].insert_many(data)
        logger.info(f"Successfully imported {len(result.inserted_ids)} documents into {collection_name}")
        return True
    except Exception as e:
        logger.error(f"Error importing data into {collection_name}: {str(e)}")
        return False

def main():
    """Main function to import data into MongoDB."""
    # Get MongoDB connection details from environment variables or use defaults
    mongo_uri = os.environ.get("MONGODB_CONNECTION_STRING", "mongodb://localhost:27017")
    db_name = os.environ.get("MONGODB_DATABASE_NAME", "chunker_service")
    
    # Define paths to JSON files
    users_json_path = "xtra/chunker_service.users.json"
    processed_docs_json_path = "xtra/chunker_service.processed_documents.json"
    
    # Connect to MongoDB
    db = connect_to_mongodb(mongo_uri, db_name)
    if not db:
        logger.error("Failed to connect to MongoDB. Exiting.")
        sys.exit(1)
    
    # Import users collection
    users_data = parse_json_file(users_json_path)
    if users_data:
        import_collection(db, "users", users_data)
    
    # Import processed_documents collection
    processed_docs_data = parse_json_file(processed_docs_json_path)
    if processed_docs_data:
        import_collection(db, "processed_documents", processed_docs_data)
    
    logger.info("MongoDB import completed")

if __name__ == "__main__":
    main()
