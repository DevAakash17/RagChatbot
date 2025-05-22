#!/bin/bash
# Script to import MongoDB data from JSON files

echo "Importing MongoDB data..."

# MongoDB connection settings - adjust these to match your Docker setup
MONGO_HOST="0.0.0.0"
MONGO_PORT="27017"
MONGO_URI="mongodb://${MONGO_HOST}:${MONGO_PORT}"

# Skip MongoDB check as it might be running in Docker
echo "Connecting to MongoDB at ${MONGO_URI}..."

# Import users collection
echo "Importing users collection..."
mongoimport --uri="${MONGO_URI}" --db chunker_service --collection users --file xtra/chunker_service.users.json --jsonArray --drop

# Import processed_documents collection
echo "Importing processed_documents collection..."
mongoimport --uri="${MONGO_URI}" --db chunker_service --collection processed_documents --file xtra/chunker_service.processed_documents.json --jsonArray --drop

echo "MongoDB import completed successfully!"
