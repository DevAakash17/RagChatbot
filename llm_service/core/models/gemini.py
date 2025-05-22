"""
Gemini model implementation.
"""
import json
from typing import Dict, Any, Optional

import aiohttp

from llm_service.core.models.base import BaseLLMModel
from llm_service.utils.errors import ModelRequestError, ModelResponseError
from llm_service.utils.logging import setup_logging


logger = setup_logging(__name__)


class GeminiModel(BaseLLMModel):
    """Gemini model implementation."""

    async def generate(self, prompt: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate text using the Gemini model.

        Args:
            prompt: Input prompt.
            options: Additional options for generation.

        Returns:
            Generated text and metadata.
        """
        options = options or {}

        # Prepare request URL with API key
        api_key = self.config.get("api_key", "")
        base_url = self.config.get("base_url", "")
        url = f"{base_url}?{self.config.get('api_key_param', 'key')}={api_key}"

        # Prepare request payload
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        # Add any additional parameters from options as generation config
        generation_config = {}
        if "temperature" in options:
            generation_config["temperature"] = options["temperature"]
        if "max_tokens" in options:
            generation_config["maxOutputTokens"] = options["max_tokens"]
        if "top_p" in options:
            generation_config["topP"] = options["top_p"]
        if "top_k" in options:
            generation_config["topK"] = options["top_k"]

        # Add generation config to payload if not empty
        if generation_config:
            payload["generationConfig"] = generation_config

        logger.info(f"Sending request to Gemini model: {self.model_name}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=self.config.get("timeout", 30)
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Gemini API error: {error_text}")
                        raise ModelResponseError(
                            message=f"Gemini API returned status {response.status}",
                            details={"status": response.status, "response": error_text}
                        )

                    response_data = await response.json()

                    # Extract the generated text from the response
                    try:
                        # Log the response structure for debugging
                        logger.debug(f"Response structure: {json.dumps(response_data)}")

                        # Extract text from the first candidate's content
                        candidate = response_data.get("candidates", [])[0]
                        content = candidate.get("content", {})
                        parts = content.get("parts", [])

                        if not parts:
                            raise KeyError("No parts found in response content")

                        generated_text = parts[0].get("text", "")

                        # Extract usage metadata if available
                        usage_metadata = response_data.get("usageMetadata", {})

                        return {
                            "text": generated_text,
                            "model": self.model_name,
                            "usage": {
                                "prompt_tokens": usage_metadata.get("promptTokenCount", 0),
                                "completion_tokens": usage_metadata.get("candidatesTokenCount", 0),
                                "total_tokens": usage_metadata.get("totalTokenCount", 0)
                            },
                            "finish_reason": candidate.get("finishReason", "STOP")
                        }
                    except (KeyError, IndexError) as e:
                        logger.error(f"Failed to parse Gemini response: {e}")
                        logger.error(f"Response data: {json.dumps(response_data)}")
                        raise ModelResponseError(
                            message="Failed to parse Gemini response",
                            details={"error": str(e), "response": response_data}
                        )

        except aiohttp.ClientError as e:
            logger.error(f"Gemini API request failed: {e}")
            raise ModelRequestError(
                message=f"Failed to connect to Gemini API: {e}",
                details={"error": str(e)}
            )
