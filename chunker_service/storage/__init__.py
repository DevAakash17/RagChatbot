"""
Storage module for the Chunker Service.
"""
from typing import Dict, Any, Optional

from chunker_service.core.config import settings
from chunker_service.core.errors import StorageError
from chunker_service.core.logging import setup_logging
from chunker_service.storage.base import BaseStorageAdapter
from chunker_service.storage.local import LocalStorageAdapter
from chunker_service.storage.s3 import S3StorageAdapter


logger = setup_logging(__name__)


async def get_storage_adapter(storage_type: Optional[str] = None, **kwargs) -> BaseStorageAdapter:
    """Get a storage adapter.

    Args:
        storage_type: Type of storage adapter
        **kwargs: Additional parameters

    Returns:
        Storage adapter instance
    """
    # Use specified storage type or default
    storage_type = storage_type or settings.STORAGE_TYPE

    logger.info(f"Creating storage adapter: {storage_type}")

    if storage_type.lower() == "local":
        return LocalStorageAdapter(
            base_path=kwargs.get("base_path", settings.STORAGE_BASE_PATH)
        )
    elif storage_type.lower() == "s3":
        return S3StorageAdapter(
            access_key=kwargs.get("access_key", settings.S3_ACCESS_KEY),
            secret_key=kwargs.get("secret_key", settings.S3_SECRET_KEY),
            region=kwargs.get("region", settings.S3_REGION),
            endpoint_url=kwargs.get("endpoint_url", settings.S3_ENDPOINT)
        )
    else:
        raise StorageError(f"Unsupported storage type: {storage_type}")
