"""
Sentence Transformers implementation of the embedding model.
"""
import torch
from typing import List, Dict, Any, Optional
from loguru import logger

from .base import BaseEmbeddingModel
from ..core.errors import EmbeddingModelError


class SentenceTransformerModel(BaseEmbeddingModel):
    """Sentence Transformers implementation of the embedding model."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", **kwargs):
        """Initialize the Sentence Transformers model.

        Args:
            model_name: Name of the model to use
            **kwargs: Additional model parameters
        """
        try:
            from sentence_transformers import SentenceTransformer
            import torch

            logger.info(f"Loading Sentence Transformers model: {model_name}")
            logger.info(f"PyTorch CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                logger.info(f"CUDA device: {torch.cuda.get_device_name(0)}")
                logger.info(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

            # Explicitly set cache directory to ensure we know where models are stored
            cache_folder = kwargs.get('cache_folder', None)
            if cache_folder:
                logger.info(f"Using custom cache folder: {cache_folder}")

            self.model_name = model_name

            # More verbose model loading
            logger.info(f"Attempting to load model: {model_name}")
            try:
                # Set a timeout for model loading
                import signal
                from contextlib import contextmanager

                @contextmanager
                def timeout(seconds):
                    def handler(signum, frame):
                        raise TimeoutError(f"Model loading timed out after {seconds} seconds")

                    # Set the timeout handler
                    signal.signal(signal.SIGALRM, handler)
                    signal.alarm(seconds)
                    try:
                        yield
                    finally:
                        # Reset the alarm
                        signal.alarm(0)

                # Try to load the model with a timeout
                logger.info(f"Loading model with a 60-second timeout")
                with timeout(60):
                    self.model = SentenceTransformer(model_name, **kwargs)

                logger.info(f"Model class: {type(self.model).__name__}")
                logger.info(f"Model successfully loaded from HuggingFace or cache")
            except Exception as model_error:
                logger.error(f"Error loading model {model_name}: {str(model_error)}")
                logger.warning(f"Falling back to default model: BAAI/bge-small-en-v1.5")
                self.model = SentenceTransformer("BAAI/bge-small-en-v1.5", **kwargs)
                self.model_name = "BAAI/bge-small-en-v1.5"  # Update model name to match actual model

            # Set device if specified
            device = kwargs.get('device')
            if device:
                logger.info(f"Moving model to device: {device}")
                self.model.to(device)
            elif torch.cuda.is_available():
                logger.info(f"Moving model to CUDA automatically")
                self.model.to('cuda')

            dimension = self.get_dimension()
            logger.info(f"Model loaded successfully with dimension: {dimension}")
            if dimension != 384 and 'bge-small' in model_name:
                logger.warning(f"Expected dimension 384 for {model_name} but got {dimension}. This suggests the model didn't load correctly.")
        except Exception as e:
            error_msg = f"Failed to initialize Sentence Transformers model: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg, details={"model_name": model_name})

    def embed(self, texts: List[str], **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts.

        Args:
            texts: List of texts to embed
            **kwargs: Additional embedding parameters

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Get embeddings
            embeddings = self.model.encode(
                texts,
                convert_to_tensor=False,
                normalize_embeddings=kwargs.get('normalize', True),
                show_progress_bar=kwargs.get('show_progress', False)
            )

            # Convert to list of lists
            return embeddings.tolist() if not isinstance(embeddings, list) else embeddings
        except Exception as e:
            error_msg = f"Failed to generate embeddings: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg)

    def get_dimension(self) -> int:
        """Get the dimension of the embeddings.

        Returns:
            Dimension of the embeddings
        """
        return self.model.get_sentence_embedding_dimension()

    def get_model_name(self) -> str:
        """Get the name of the model.

        Returns:
            Name of the model
        """
        return self.model_name

    def batch_embed(self, texts: List[str], batch_size: int = 32, **kwargs) -> List[List[float]]:
        """Generate embeddings for a list of texts in batches.

        Args:
            texts: List of texts to embed
            batch_size: Size of each batch
            **kwargs: Additional embedding parameters

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        try:
            # Get embeddings in batches
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_tensor=False,
                normalize_embeddings=kwargs.get('normalize', True),
                show_progress_bar=kwargs.get('show_progress', False)
            )

            # Convert to list of lists
            return embeddings.tolist() if not isinstance(embeddings, list) else embeddings
        except Exception as e:
            error_msg = f"Failed to generate batch embeddings: {str(e)}"
            logger.error(error_msg)
            raise EmbeddingModelError(message=error_msg, details={"batch_size": batch_size})
