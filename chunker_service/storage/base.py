"""
Base class for storage adapters.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, BinaryIO, AsyncGenerator, Union
from io import BytesIO


class BaseStorageAdapter(ABC):
    """Abstract base class for storage adapters."""
    
    @abstractmethod
    def __init__(self, **kwargs):
        """Initialize the storage adapter.
        
        Args:
            **kwargs: Storage-specific parameters
        """
        pass
    
    @abstractmethod
    async def list_objects(self, path: str) -> List[Dict[str, Any]]:
        """List objects in a path.
        
        Args:
            path: Path to list objects from
            
        Returns:
            List of object information
        """
        pass
    
    @abstractmethod
    async def get_object(self, path: str) -> BytesIO:
        """Get an object.
        
        Args:
            path: Path to the object
            
        Returns:
            Object data as BytesIO
        """
        pass
    
    @abstractmethod
    async def stream_object(self, path: str) -> AsyncGenerator[bytes, None]:
        """Stream an object.
        
        Args:
            path: Path to the object
            
        Returns:
            Async generator yielding chunks of the object
        """
        pass
    
    @abstractmethod
    async def get_object_metadata(self, path: str) -> Dict[str, Any]:
        """Get object metadata.
        
        Args:
            path: Path to the object
            
        Returns:
            Object metadata
        """
        pass
    
    @abstractmethod
    async def object_exists(self, path: str) -> bool:
        """Check if an object exists.
        
        Args:
            path: Path to the object
            
        Returns:
            True if the object exists, False otherwise
        """
        pass
    
    @abstractmethod
    async def get_text_content(self, path: str, encoding: str = "utf-8") -> str:
        """Get text content of an object.
        
        Args:
            path: Path to the object
            encoding: Text encoding
            
        Returns:
            Text content
        """
        pass
