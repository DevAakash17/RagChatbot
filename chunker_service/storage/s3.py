"""
S3 storage adapter.
"""
import os
import asyncio
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any, Optional, AsyncGenerator

from chunker_service.core.logging import setup_logging
from chunker_service.core.errors import StorageError, ResourceNotFoundError
from chunker_service.storage.base import BaseStorageAdapter


logger = setup_logging(__name__)


class S3StorageAdapter(BaseStorageAdapter):
    """S3 storage adapter."""

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        region: str = "us-east-1",
        endpoint_url: Optional[str] = None,
        **kwargs
    ):
        """Initialize the S3 storage adapter.

        Args:
            access_key: AWS access key
            secret_key: AWS secret key
            region: AWS region
            endpoint_url: Custom endpoint URL for S3-compatible services
            **kwargs: Additional parameters
        """
        try:
            import aioboto3

            self.access_key = access_key
            self.secret_key = secret_key
            self.region = region
            self.endpoint_url = endpoint_url

            # Create session
            self.session = aioboto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )

            logger.info(f"Initialized S3StorageAdapter for region: {region}")
        except ImportError:
            error_msg = "aioboto3 is required for S3 storage. Install with 'pip install aioboto3'"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
        except Exception as e:
            error_msg = f"Failed to initialize S3StorageAdapter: {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)

    async def list_objects(self, path: str) -> List[Dict[str, Any]]:
        """List objects in a path.

        Args:
            path: Path to list objects from (bucket/prefix)

        Returns:
            List of object information
        """
        try:
            # Split bucket and prefix
            parts = path.strip("/").split("/", 1)
            bucket = parts[0]
            prefix = parts[1] + "/" if len(parts) > 1 else ""

            # Create S3 client
            async with self.session.client(
                "s3",
                endpoint_url=self.endpoint_url
            ) as s3:
                # Check if bucket exists
                try:
                    await s3.head_bucket(Bucket=bucket)
                except Exception as e:
                    raise ResourceNotFoundError(f"Bucket not found: {bucket}")

                # List objects
                paginator = s3.get_paginator("list_objects_v2")
                objects = []

                async for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter="/"):
                    # Add common prefixes (directories)
                    for prefix_entry in page.get("CommonPrefixes", []):
                        prefix_path = prefix_entry.get("Prefix")
                        objects.append({
                            "name": os.path.basename(prefix_path.rstrip("/")),
                            "path": f"{bucket}/{prefix_path}",
                            "size": 0,
                            "last_modified": None,
                            "is_dir": True
                        })

                    # Add objects (files)
                    for obj in page.get("Contents", []):
                        # Skip the prefix itself
                        if obj.get("Key") == prefix:
                            continue

                        objects.append({
                            "name": os.path.basename(obj.get("Key")),
                            "path": f"{bucket}/{obj.get('Key')}",
                            "size": obj.get("Size", 0),
                            "last_modified": obj.get("LastModified").isoformat() if obj.get("LastModified") else None,
                            "is_dir": False
                        })

            logger.info(f"Listed {len(objects)} objects in path: {path}")
            return objects
        except ResourceNotFoundError as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to list objects in path '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)

    async def get_object(self, path: str) -> BytesIO:
        """Get an object.

        Args:
            path: Path to the object (bucket/key)

        Returns:
            Object data as BytesIO
        """
        try:
            # Split bucket and key
            parts = path.strip("/").split("/", 1)
            if len(parts) < 2:
                raise ValidationError(f"Invalid path format: {path}. Expected format: bucket/key")

            bucket = parts[0]
            key = parts[1]

            # Create S3 client
            async with self.session.client(
                "s3",
                endpoint_url=self.endpoint_url
            ) as s3:
                try:
                    response = await s3.get_object(Bucket=bucket, Key=key)
                except s3.exceptions.NoSuchKey:
                    raise ResourceNotFoundError(f"Object not found: {path}")

                # Read object data
                data = await response["Body"].read()

                logger.info(f"Retrieved object: {path} ({len(data)} bytes)")
                return BytesIO(data)
        except ResourceNotFoundError as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to get object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)

    async def stream_object(self, path: str, chunk_size: int = 8192) -> AsyncGenerator[bytes, None]:
        """Stream an object.

        Args:
            path: Path to the object (bucket/key)
            chunk_size: Size of each chunk in bytes

        Returns:
            Async generator yielding chunks of the object
        """
        try:
            # Split bucket and key
            parts = path.strip("/").split("/", 1)
            if len(parts) < 2:
                raise ValidationError(f"Invalid path format: {path}. Expected format: bucket/key")

            bucket = parts[0]
            key = parts[1]

            # Create S3 client
            async with self.session.client(
                "s3",
                endpoint_url=self.endpoint_url
            ) as s3:
                try:
                    response = await s3.get_object(Bucket=bucket, Key=key)
                except s3.exceptions.NoSuchKey:
                    raise ResourceNotFoundError(f"Object not found: {path}")

                # Stream object data
                stream = response["Body"]
                while True:
                    chunk = await stream.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

                logger.info(f"Streamed object: {path}")
        except ResourceNotFoundError as e:
            # Re-raise known errors
            raise
        except Exception as e:
            error_msg = f"Failed to stream object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)

    async def get_object_metadata(self, path: str) -> Dict[str, Any]:
        """Get object metadata.

        Args:
            path: Path to the object (bucket/key)

        Returns:
            Object metadata
        """
        try:
            # Split bucket and key
            parts = path.strip("/").split("/", 1)
            if len(parts) < 2:
                raise ValidationError(f"Invalid path format: {path}. Expected format: bucket/key")

            bucket = parts[0]
            key = parts[1]

            # Create S3 client
            async with self.session.client(
                "s3",
                endpoint_url=self.endpoint_url
            ) as s3:
                try:
                    response = await s3.head_object(Bucket=bucket, Key=key)
                except s3.exceptions.NoSuchKey:
                    raise ResourceNotFoundError(f"Object not found: {path}")

                # Extract metadata
                metadata = {
                    "name": os.path.basename(key),
                    "path": path,
                    "size": response.get("ContentLength", 0),
                    "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
                    "is_dir": False,
                    "content_type": response.get("ContentType", "application/octet-stream"),
                    "etag": response.get("ETag"),
                    "metadata": response.get("Metadata", {})
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
            path: Path to the object (bucket/key)

        Returns:
            True if the object exists, False otherwise
        """
        try:
            # Split bucket and key
            parts = path.strip("/").split("/", 1)
            if len(parts) < 2:
                return False

            bucket = parts[0]
            key = parts[1]

            # Create S3 client
            async with self.session.client(
                "s3",
                endpoint_url=self.endpoint_url
            ) as s3:
                try:
                    await s3.head_object(Bucket=bucket, Key=key)
                    return True
                except:
                    return False
        except Exception:
            return False

    async def get_text_content(self, path: str, encoding: str = "utf-8") -> str:
        """Get text content of an object.

        Args:
            path: Path to the object (bucket/key)
            encoding: Text encoding

        Returns:
            Text content
        """
        try:
            # Get object
            data = await self.get_object(path)

            # Decode content
            content = data.getvalue().decode(encoding)

            logger.info(f"Retrieved text content for object: {path} ({len(content)} characters)")
            return content
        except UnicodeDecodeError as e:
            error_msg = f"Failed to decode object '{path}' with encoding '{encoding}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
        except Exception as e:
            if isinstance(e, StorageError) or isinstance(e, ResourceNotFoundError):
                raise

            error_msg = f"Failed to get text content for object '{path}': {str(e)}"
            logger.error(error_msg)
            raise StorageError(message=error_msg)
