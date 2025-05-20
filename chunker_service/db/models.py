"""
Database models for the Chunker Service.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib
import json


class ProcessedDocument:
    """Model for a processed document."""
    
    def __init__(
        self,
        document_path: str,
        collection_name: str,
        document_hash: str,
        chunk_count: int,
        chunk_ids: List[str],
        chunking_strategy: str,
        chunking_config: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
        processed_at: Optional[datetime] = None
    ):
        """Initialize a processed document.
        
        Args:
            document_path: Path to the document
            collection_name: Name of the collection where embeddings are stored
            document_hash: Hash of the document content
            chunk_count: Number of chunks created
            chunk_ids: IDs of the chunks in the vector database
            chunking_strategy: Chunking strategy used
            chunking_config: Configuration of the chunking strategy
            metadata: Additional metadata
            processed_at: Timestamp when the document was processed
        """
        self.document_path = document_path
        self.collection_name = collection_name
        self.document_hash = document_hash
        self.chunk_count = chunk_count
        self.chunk_ids = chunk_ids
        self.chunking_strategy = chunking_strategy
        self.chunking_config = chunking_config
        self.metadata = metadata or {}
        self.processed_at = processed_at or datetime.utcnow()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProcessedDocument':
        """Create a ProcessedDocument from a dictionary.
        
        Args:
            data: Dictionary representation of a processed document
            
        Returns:
            ProcessedDocument instance
        """
        # Convert string timestamp to datetime if needed
        processed_at = data.get('processed_at')
        if isinstance(processed_at, str):
            processed_at = datetime.fromisoformat(processed_at)
        
        return cls(
            document_path=data['document_path'],
            collection_name=data['collection_name'],
            document_hash=data['document_hash'],
            chunk_count=data['chunk_count'],
            chunk_ids=data['chunk_ids'],
            chunking_strategy=data['chunking_strategy'],
            chunking_config=data['chunking_config'],
            metadata=data.get('metadata', {}),
            processed_at=processed_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            'document_path': self.document_path,
            'collection_name': self.collection_name,
            'document_hash': self.document_hash,
            'chunk_count': self.chunk_count,
            'chunk_ids': self.chunk_ids,
            'chunking_strategy': self.chunking_strategy,
            'chunking_config': self.chunking_config,
            'metadata': self.metadata,
            'processed_at': self.processed_at.isoformat()
        }
    
    @staticmethod
    def calculate_hash(content: bytes) -> str:
        """Calculate a hash for document content.
        
        Args:
            content: Document content
            
        Returns:
            Hash string
        """
        return hashlib.sha256(content).hexdigest()
    
    def __str__(self) -> str:
        """String representation.
        
        Returns:
            String representation
        """
        return f"ProcessedDocument(path={self.document_path}, collection={self.collection_name}, chunks={self.chunk_count})"
