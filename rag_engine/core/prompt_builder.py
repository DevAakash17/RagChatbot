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
        context_documents: List[Dict[str, Any]],
        prev_queries: Optional[List[str]] = None
    ) -> str:
        """Build a prompt with the query, context, and previous queries.

        Args:
            query: User query
            context_documents: Retrieved context documents
            prev_queries: Optional list of previous queries for context

        Returns:
            Constructed prompt
        """
        logger.info(f"Building prompt for query: {query}")

        # Format context documents
        context_str = self._format_context(context_documents)

        # Format previous queries if available
        prev_queries_str = self._format_prev_queries(prev_queries or [])

        # Fill in the template
        prompt = self.template.format(
            query=query,
            context=context_str,
            prev_queries=prev_queries_str
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

    def _format_prev_queries(self, prev_queries: List[str]) -> str:
        """Format previous queries into a string.

        Args:
            prev_queries: List of previous queries

        Returns:
            Formatted previous queries string
        """
        if not prev_queries:
            return "No previous queries."

        # Format each previous query
        formatted_queries = []
        for i, query in enumerate(prev_queries):
            formatted_queries.append(f"Query {i+1}: {query}")

        # Join all formatted queries
        return "\n".join(formatted_queries)
