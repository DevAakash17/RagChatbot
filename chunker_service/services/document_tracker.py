"""
Service for tracking processed documents.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib

from chunker_service.core.config import settings
from chunker_service.core.logging import setup_logging
from chunker_service.core.errors import DatabaseError
from chunker_service.db import get_mongodb_client
from chunker_service.db.models import ProcessedDocument


logger = setup_logging(__name__)


class DocumentTracker:
    """Service for tracking processed documents."""
    
    def __init__(self, collection_name: Optional[str] = None):
        """Initialize the document tracker.
        
        Args:
            collection_name: Name of the MongoDB collection to use
        """
        self.collection_name = collection_name or settings.MONGODB_DOCUMENT_COLLECTION
        logger.info(f"Initialized DocumentTracker with collection: {self.collection_name}")
    
    async def is_document_processed(
        self,
        document_path: str,
        content_hash: Optional[str] = None
    ) -> bool:
        """Check if a document has already been processed.
        
        Args:
            document_path: Path to the document
            content_hash: Optional hash of the document content
            
        Returns:
            True if the document has been processed, False otherwise
        """
        try:
            # Get MongoDB client
            mongodb = await get_mongodb_client()
            
            # Build query
            query = {"document_path": document_path}
            
            # If hash is provided, check if the document has changed
            if content_hash:
                query["document_hash"] = content_hash
            
            # Check if document exists
            document = await mongodb.find_document(self.collection_name, query)
            
            if document:
                logger.info(f"Document already processed: {document_path}")
                return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking if document is processed: {str(e)}")
            return False
    
    async def track_document(self, document: ProcessedDocument) -> bool:
        """Track a processed document.
        
        Args:
            document: Processed document to track
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get MongoDB client
            mongodb = await get_mongodb_client()
            
            # Convert document to dictionary
            document_dict = document.to_dict()
            
            # Check if document already exists
            existing = await mongodb.find_document(
                self.collection_name,
                {"document_path": document.document_path}
            )
            
            if existing:
                # Update existing document
                await mongodb.update_document(
                    self.collection_name,
                    {"document_path": document.document_path},
                    {"$set": document_dict}
                )
                logger.info(f"Updated tracking for document: {document.document_path}")
            else:
                # Insert new document
                await mongodb.insert_document(self.collection_name, document_dict)
                logger.info(f"Added tracking for document: {document.document_path}")
            
            return True
        except Exception as e:
            logger.error(f"Error tracking document: {str(e)}")
            return False
    
    async def get_processed_document(self, document_path: str) -> Optional[ProcessedDocument]:
        """Get a processed document.
        
        Args:
            document_path: Path to the document
            
        Returns:
            ProcessedDocument if found, None otherwise
        """
        try:
            # Get MongoDB client
            mongodb = await get_mongodb_client()
            
            # Find document
            document_dict = await mongodb.find_document(
                self.collection_name,
                {"document_path": document_path}
            )
            
            if document_dict:
                return ProcessedDocument.from_dict(document_dict)
            
            return None
        except Exception as e:
            logger.error(f"Error getting processed document: {str(e)}")
            return None
    
    async def list_processed_documents(
        self,
        collection_name: Optional[str] = None,
        limit: int = 100
    ) -> List[ProcessedDocument]:
        """List processed documents.
        
        Args:
            collection_name: Optional collection name filter
            limit: Maximum number of documents to return
            
        Returns:
            List of processed documents
        """
        try:
            # Get MongoDB client
            mongodb = await get_mongodb_client()
            
            # Build query
            query = {}
            if collection_name:
                query["collection_name"] = collection_name
            
            # Find documents
            documents = await mongodb.find_documents(
                self.collection_name,
                query,
                sort=[("processed_at", -1)],
                limit=limit
            )
            
            # Convert to ProcessedDocument objects
            return [ProcessedDocument.from_dict(doc) for doc in documents]
        except Exception as e:
            logger.error(f"Error listing processed documents: {str(e)}")
            return []
    
    @staticmethod
    async def calculate_document_hash(content: bytes) -> str:
        """Calculate a hash for document content.
        
        Args:
            content: Document content
            
        Returns:
            Hash string
        """
        return ProcessedDocument.calculate_hash(content)
