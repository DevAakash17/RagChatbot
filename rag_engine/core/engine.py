"""
Core RAG Engine implementation.
"""
from typing import Dict, Any, Optional, List

from chatbot.rag_engine.core.config import settings
from chatbot.rag_engine.core.query_processor import QueryProcessor
from chatbot.rag_engine.core.context_retriever import ContextRetriever
from chatbot.rag_engine.core.prompt_builder import PromptBuilder
from chatbot.rag_engine.core.response_generator import ResponseGenerator
from chatbot.rag_engine.services.embedding_client import EmbeddingClient
from chatbot.rag_engine.services.llm_client import LLMClient
from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class RAGEngine:
    """Main RAG Engine class."""
    
    def __init__(
        self,
        embedding_client: Optional[EmbeddingClient] = None,
        llm_client: Optional[LLMClient] = None
    ):
        """Initialize the RAG Engine.
        
        Args:
            embedding_client: Optional embedding client
            llm_client: Optional LLM client
        """
        # Initialize clients
        self.embedding_client = embedding_client or EmbeddingClient()
        self.llm_client = llm_client or LLMClient()
        
        # Initialize components
        self.query_processor = QueryProcessor()
        self.context_retriever = ContextRetriever(self.embedding_client)
        self.prompt_builder = PromptBuilder()
        self.response_generator = ResponseGenerator(self.llm_client)
        
        logger.info("Initialized RAGEngine")
    
    async def process(
        self,
        query: str,
        collection_name: Optional[str] = None,
        llm_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        llm_options: Optional[Dict[str, Any]] = None,
        top_k: Optional[int] = None
    ) -> Dict[str, Any]:
        """Process a query through the RAG pipeline.
        
        Args:
            query: User query
            collection_name: Name of the collection to query
            llm_model: Optional LLM model to use
            embedding_model: Optional embedding model to use
            llm_options: Optional LLM generation options
            top_k: Number of context documents to retrieve
            
        Returns:
            Generated response and metadata
        """
        logger.info(f"Processing query: {query}")
        
        # Process the query
        processed_query = self.query_processor.process_query(query)
        
        # Retrieve context
        context_documents = await self.context_retriever.retrieve_context(
            query=processed_query,
            collection_name=collection_name,
            top_k=top_k,
            model=embedding_model
        )
        
        # Build prompt
        prompt = self.prompt_builder.build_prompt(
            query=query,  # Use original query in the prompt
            context_documents=context_documents
        )
        
        # Generate response
        response = await self.response_generator.generate_response(
            prompt=prompt,
            model=llm_model,
            options=llm_options
        )
        
        # Add context documents to the response
        response["context_documents"] = context_documents
        
        logger.info("Query processing completed successfully")
        return response
