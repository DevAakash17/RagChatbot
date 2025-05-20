"""
Prompt builder for the RAG Engine.
"""
from typing import List, Dict, Any, Optional

from chatbot.rag_engine.core.config import settings
from chatbot.rag_engine.utils.logging import setup_logging


logger = setup_logging(__name__)


class PromptBuilder:
    """Builds prompts with retrieved context."""
    
    def __init__(self, template: Optional[str] = None):
        """Initialize the prompt builder.
        
        Args:
            template: Optional prompt template
        """
        self.template = template or settings.PROMPT_TEMPLATE
        logger.info("Initialized PromptBuilder")
    
    def build_prompt(
        self,
        query: str,
        context_documents: List[Dict[str, Any]]
    ) -> str:
        """Build a prompt with the query and context.
        
        Args:
            query: User query
            context_documents: Retrieved context documents
            
        Returns:
            Constructed prompt
        """
        logger.info(f"Building prompt for query: {query}")
        
        # Format context documents
        context_str = self._format_context(context_documents)
        
        # Fill in the template
        prompt = self.template.format(
            query=query,
            context=context_str
        )
        
        logger.debug(f"Built prompt: {prompt}")
        return prompt
    
    def _format_context(self, documents: List[Dict[str, Any]]) -> str:
        """Format context documents into a string.
        
        Args:
            documents: List of context documents
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant context found."
        
        # Format each document
        formatted_docs = []
        for i, doc in enumerate(documents):
            formatted_doc = f"Document {i+1}:\n{doc['text']}\n"
            
            # Add metadata if available
            if doc.get("metadata"):
                metadata_str = ", ".join(f"{k}: {v}" for k, v in doc["metadata"].items())
                formatted_doc += f"Metadata: {metadata_str}\n"
            
            formatted_docs.append(formatted_doc)
        
        # Join all formatted documents
        return "\n".join(formatted_docs)
