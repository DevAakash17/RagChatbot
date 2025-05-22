"""
Test script for the Gemini model.
"""
import asyncio
import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_service.core.models.gemini import GeminiModel
from llm_service.utils.errors import ModelResponseError


class TestGeminiModel(unittest.TestCase):
    """Test cases for the Gemini model."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.model_name = "gemini-2.0-flash"
        self.config = {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
            "api_key_param": "key",
            "api_key": "test_api_key",
            "timeout": 30
        }
        self.model = GeminiModel(self.model_name, self.config)
        
    @patch('aiohttp.ClientSession.post')
    async def test_generate_success(self, mock_post):
        """Test successful text generation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "This is a test response"
                            }
                        ]
                    },
                    "finishReason": "STOP"
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 10,
                "candidatesTokenCount": 20,
                "totalTokenCount": 30
            }
        }
        
        # Configure mock
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # Call the method
        result = await self.model.generate("Test prompt")
        
        # Assertions
        self.assertEqual(result["text"], "This is a test response")
        self.assertEqual(result["model"], self.model_name)
        self.assertEqual(result["usage"]["prompt_tokens"], 10)
        self.assertEqual(result["usage"]["completion_tokens"], 20)
        self.assertEqual(result["usage"]["total_tokens"], 30)
        self.assertEqual(result["finish_reason"], "STOP")
        
    @patch('aiohttp.ClientSession.post')
    async def test_generate_error(self, mock_post):
        """Test error handling in text generation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = 400
        mock_response.text.return_value = json.dumps({
            "error": {
                "code": 400,
                "message": "Invalid request",
                "status": "INVALID_ARGUMENT"
            }
        })
        
        # Configure mock
        mock_post.return_value.__aenter__.return_value = mock_response
        
        # Call the method and expect exception
        with self.assertRaises(ModelResponseError):
            await self.model.generate("Test prompt")


def run_tests():
    """Run the tests."""
    unittest.main()


if __name__ == "__main__":
    # Create test directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    # Run tests
    run_tests()
