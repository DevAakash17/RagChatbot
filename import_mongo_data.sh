#!/bin/bash
# Script to import MongoDB data from JSON files

echo "Importing MongoDB data..."

# Check if MongoDB is running
if ! mongosh --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
  echo "Error: MongoDB is not running. Please start MongoDB first."
  exit 1
fi

# Import users collection
echo "Importing users collection..."
mongoimport --db chunker_service --collection users --file xtra/chunker_service.users.json --jsonArray

# Import processed_documents collection
echo "Importing processed_documents collection..."
mongoimport --db chunker_service --collection processed_documents --file xtra/chunker_service.processed_documents.json --jsonArray

echo "MongoDB import completed successfully!"
