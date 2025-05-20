"""
MongoDB client for the Chunker Service.
"""
import os
from typing import Dict, Any, Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError

from chatbot.chunker_service.core.config import settings
from chatbot.chunker_service.core.logging import setup_logging
from chatbot.chunker_service.core.errors import DatabaseError

logger = setup_logging(__name__)

class MongoDBClient:
    """MongoDB client for the Chunker Service."""
    
    def __init__(
        self,
        connection_string: Optional[str] = None,
        database_name: Optional[str] = None
    ):
        """Initialize the MongoDB client.
        
        Args:
            connection_string: MongoDB connection string
            database_name: MongoDB database name
        """
        self.connection_string = connection_string or settings.MONGODB_CONNECTION_STRING
        self.database_name = database_name or settings.MONGODB_DATABASE_NAME
        self.client = None
        self.db = None
        
        logger.info(f"Initializing MongoDB client for database: {self.database_name}")
    
    async def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(self.connection_string)
            self.db = self.client[self.database_name]
            logger.info("Connected to MongoDB")
        except PyMongoError as e:
            error_msg = f"Failed to connect to MongoDB: {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
    
    async def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")
    
    async def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a document into a collection.
        
        Args:
            collection: Collection name
            document: Document to insert
            
        Returns:
            ID of the inserted document
        """
        try:
            result = await self.db[collection].insert_one(document)
            logger.info(f"Inserted document into collection '{collection}' with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            error_msg = f"Failed to insert document into collection '{collection}': {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
    
    async def find_document(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a document in a collection.
        
        Args:
            collection: Collection name
            query: Query to find the document
            
        Returns:
            Document if found, None otherwise
        """
        try:
            document = await self.db[collection].find_one(query)
            return document
        except PyMongoError as e:
            error_msg = f"Failed to find document in collection '{collection}': {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
    
    async def update_document(
        self,
        collection: str,
        query: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> bool:
        """Update a document in a collection.
        
        Args:
            collection: Collection name
            query: Query to find the document
            update: Update to apply
            upsert: Whether to insert if not found
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self.db[collection].update_one(query, update, upsert=upsert)
            logger.info(f"Updated {result.modified_count} document(s) in collection '{collection}'")
            return result.modified_count > 0 or (upsert and result.upserted_id is not None)
        except PyMongoError as e:
            error_msg = f"Failed to update document in collection '{collection}': {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
    
    async def delete_document(self, collection: str, query: Dict[str, Any]) -> bool:
        """Delete a document from a collection.
        
        Args:
            collection: Collection name
            query: Query to find the document
            
        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self.db[collection].delete_one(query)
            logger.info(f"Deleted {result.deleted_count} document(s) from collection '{collection}'")
            return result.deleted_count > 0
        except PyMongoError as e:
            error_msg = f"Failed to delete document from collection '{collection}': {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
    
    async def find_documents(
        self,
        collection: str,
        query: Dict[str, Any],
        projection: Optional[Dict[str, Any]] = None,
        sort: Optional[List[tuple]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Find documents in a collection.
        
        Args:
            collection: Collection name
            query: Query to find documents
            projection: Fields to include/exclude
            sort: Fields to sort by
            limit: Maximum number of documents to return
            
        Returns:
            List of documents
        """
        try:
            cursor = self.db[collection].find(query, projection)
            
            if sort:
                cursor = cursor.sort(sort)
            
            if limit:
                cursor = cursor.limit(limit)
            
            documents = await cursor.to_list(length=limit or 1000)
            return documents
        except PyMongoError as e:
            error_msg = f"Failed to find documents in collection '{collection}': {str(e)}"
            logger.error(error_msg)
            raise DatabaseError(message=error_msg)
