#!/bin/bash
# Script to import MongoDB data from JSON files directly into the Docker container

echo "Importing MongoDB data into Docker container..."

# Get the MongoDB container name or ID
MONGO_CONTAINER=$(docker ps --filter "name=mongodb" --format "{{.Names}}")

if [ -z "$MONGO_CONTAINER" ]; then
  echo "Error: MongoDB container not found. Make sure it's running."
  echo "You can check running containers with: docker ps"
  exit 1
fi

echo "Found MongoDB container: $MONGO_CONTAINER"

# Copy JSON files to the container
echo "Copying JSON files to container..."
docker cp xtra/chunker_service.users.json $MONGO_CONTAINER:/tmp/
docker cp xtra/chunker_service.processed_documents.json $MONGO_CONTAINER:/tmp/

# Import the data using mongoimport inside the container
echo "Importing users collection..."
docker exec $MONGO_CONTAINER mongoimport --db chunker_service --collection users --file /tmp/chunker_service.users.json --jsonArray --drop

echo "Importing processed_documents collection..."
docker exec $MONGO_CONTAINER mongoimport --db chunker_service --collection processed_documents --file /tmp/chunker_service.processed_documents.json --jsonArray --drop

echo "MongoDB import completed successfully!"
