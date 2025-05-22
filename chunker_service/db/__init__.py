"""
Database module for the Chunker Service.
"""
from typing import Optional

from chunker_service.core.config import settings
from chunker_service.core.logging import setup_logging
from chunker_service.db.mongodb import MongoDBClient

logger = setup_logging(__name__)

# Global MongoDB client instance
_mongodb_client = None

async def get_mongodb_client(
    connection_string: Optional[str] = None,
    database_name: Optional[str] = None
) -> MongoDBClient:
    """Get the MongoDB client instance.
    
    Args:
        connection_string: MongoDB connection string
        database_name: MongoDB database name
        
    Returns:
        MongoDB client instance
    """
    global _mongodb_client
    
    if _mongodb_client is None:
        _mongodb_client = MongoDBClient(
            connection_string=connection_string,
            database_name=database_name
        )
        await _mongodb_client.connect()
    
    return _mongodb_client
