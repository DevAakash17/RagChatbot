"""
Example script to demonstrate usage of the LLM service.
"""
import asyncio
import json
import os

import aiohttp


async def generate_text():
    """Example of using the LLM service API."""
    url = "http://localhost:8001/api/v1/generate"

    payload = {
        "prompt": "Explain how AI works in simple terms",
        "model": "gemini-2.0-flash",
        "options": {
            "temperature": 0.7,
            "max_tokens": 500,
            "top_p": 0.95,
            "top_k": 40
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                print("Generated Text:")
                print("-" * 50)
                print(result["text"])
                print("-" * 50)
                print(f"Model: {result['model']}")
                print(f"Token Usage: {json.dumps(result['usage'])}")
                print(f"Finish Reason: {result['finish_reason']}")
            else:
                error = await response.json()
                print(f"Error: {error['message']}")
                print(f"Status Code: {error['status_code']}")
                if error.get('details'):
                    print(f"Details: {json.dumps(error['details'])}")


if __name__ == "__main__":
    asyncio.run(generate_text())
