"""
Local filesystem storage adapter.
"""
import os
import aiofiles
import asyncio
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Optional, AsyncGenerator

from chatbot.chunker_service.core.logging import setup_logging
from chatbot.chunker_service.core.errors import StorageError, ResourceNotFoundError
from chatbot.chunker_service.storage.base import BaseStorageAdapter


logger = setup_logging(__name__)


class LocalStorageAdapter(BaseStorageAdapter):
    """Local filesystem storage adapter."""
    
    def __init__(self, base_path: str = "./storage_data", **kwargs):
        """Initialize the local storage adapter.
        
        Args:
            base_path: Base path for storage
            **kwargs: Additional parameters
        """
        self.base_path = base_path
        
        # Create base directory if it doesn't exist
        os.makedirs(self.base_path, exist_ok=True)
        
        logger.info(f"Initialized LocalStorageAdapter with base path: {self.base_path}")

    async def list_objects(self, path: str) -> List[Dict[str, Any]]:
        """List objects in a path.
        
        Args:
            path: Path to list objects from
            
        Returns:
            List of object information
        """
        full_path = os.path.join(self.base_path, path)
        
        try:
            # Check if path exists
            if not os.path.exists(full_path):
                raise ResourceNotFoundError(f"Path not found: {path}")
            
            # Check if path is a directory
            if not os.path.isdir(full_path):
                raise StorageError(f"Path is not a directory: {path}")
            
            # List objects
            objects = []
            for item in os.listdir(full_path):
                item_path = os.path.join(full_path, item)
                item_stat = os.stat(item_path)
                
                objects.append({
                    "name": item,
                    "path": os.path.join(path, item),
                    "size": item_stat.st_size,
                    "last_modified": datetime.fromtimestamp(item_stat.st_mtime).isoformat(),
                    "is_dir": os.path.isdir(item_path)
                })
            
            logger.info(f"Listed {len(objects)} objects in path: {path}")
            return objects
        except (ResourceNotFoundError, StorageError) as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to list objects in path '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
    
    async def get_object(self, path: str) -> BytesIO:
        """Get an object.
        
        Args:
            path: Path to the object
            
        Returns:
            Object data as BytesIO
        """
        full_path = os.path.join(self.base_path, path)
        
        try:
            # Check if object exists
            if not os.path.exists(full_path):
                raise ResourceNotFoundError(f"Object not found: {path}")
            
            # Check if object is a file
            if not os.path.isfile(full_path):
                raise StorageError(f"Object is not a file: {path}")
            
            # Read file
            async with aiofiles.open(full_path, "rb") as f:
                data = await f.read()
            
            logger.info(f"Retrieved object: {path} ({len(data)} bytes)")
            return BytesIO(data)
        except (ResourceNotFoundError, StorageError) as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to get object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
    
    async def stream_object(self, path: str, chunk_size: int = 8192) -> AsyncGenerator[bytes, None]:
        """Stream an object.
        
        Args:
            path: Path to the object
            chunk_size: Size of each chunk in bytes
            
        Returns:
            Async generator yielding chunks of the object
        """
        full_path = os.path.join(self.base_path, path)
        
        try:
            # Check if object exists
            if not os.path.exists(full_path):
                raise ResourceNotFoundError(f"Object not found: {path}")
            
            # Check if object is a file
            if not os.path.isfile(full_path):
                raise StorageError(f"Object is not a file: {path}")
            
            # Stream file
            async with aiofiles.open(full_path, "rb") as f:
                while True:
                    chunk = await f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
            
            logger.info(f"Streamed object: {path}")
        except (ResourceNotFoundError, StorageError) as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to stream object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
    
    async def get_object_metadata(self, path: str) -> Dict[str, Any]:
        """Get object metadata.
        
        Args:
            path: Path to the object
            
        Returns:
            Object metadata
        """
        full_path = os.path.join(self.base_path, path)
        
        try:
            # Check if object exists
            if not os.path.exists(full_path):
                raise ResourceNotFoundError(f"Object not found: {path}")
            
            # Get metadata
            stat = os.stat(full_path)
            
            metadata = {
                "name": os.path.basename(path),
                "path": path,
                "size": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "is_dir": os.path.isdir(full_path),
                "content_type": self._guess_content_type(path)
            }
            
            logger.info(f"Retrieved metadata for object: {path}")
            return metadata
        except ResourceNotFoundError as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to get metadata for object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
    
    async def object_exists(self, path: str) -> bool:
        """Check if an object exists.
        
        Args:
            path: Path to the object
            
        Returns:
            True if the object exists, False otherwise
        """
        full_path = os.path.join(self.base_path, path)
        return os.path.exists(full_path)
    
    async def get_text_content(self, path: str, encoding: str = "utf-8") -> str:
        """Get text content of an object.
        
        Args:
            path: Path to the object
            encoding: Text encoding
            
        Returns:
            Text content
        """
        full_path = os.path.join(self.base_path, path)
        
        try:
            # Check if object exists
            if not os.path.exists(full_path):
                raise ResourceNotFoundError(f"Object not found: {path}")
            
            # Check if object is a file
            if not os.path.isfile(full_path):
                raise StorageError(f"Object is not a file: {path}")
            
            # Read file
            async with aiofiles.open(full_path, "r", encoding=encoding) as f:
                content = await f.read()
            
            logger.info(f"Retrieved text content for object: {path} ({len(content)} characters)")
            return content
        except (ResourceNotFoundError, StorageError) as e:
            # Re-raise known errors
            raise
        except UnicodeDecodeError as e:
            error_msg = f"Failed to decode object '{path}' with encoding '{encoding}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
        except Exception as e:
            error_msg = f"Failed to get text content for object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
    
    def _guess_content_type(self, path: str) -> str:
        """Guess content type based on file extension.
        
        Args:
            path: Path to the object
            
        Returns:
            Content type
        """
        # Simple mapping of extensions to content types
        extension_map = {
            ".txt": "text/plain",
            ".pdf": "application/pdf",
            ".json": "application/json",
            ".csv": "text/csv",
            ".md": "text/markdown",
            ".html": "text/html",
            ".htm": "text/html",
            ".xml": "application/xml",
            ".doc": "application/msword",
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".xls": "application/vnd.ms-excel",
            ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            ".ppt": "application/vnd.ms-powerpoint",
            ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        }
        
        # Get file extension
        _, ext = os.path.splitext(path.lower())
        
        # Return content type or default
        return extension_map.get(ext, "application/octet-stream")
