import os
from typing import Optional, Dict, Any, Literal
import requests
import tiktoken
from dotenv import load_dotenv

load_dotenv()

class GoLean:
    """Client for interacting with the GoLean API."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the GoLean client.

        Args:
            api_key (str, optional): The API key for authentication. If not provided,
                                     it will be read from the GOLEAN_API_KEY environment variable.

        Raises:
            ValueError: If the API key is not provided and not found in environment variables.
        """
        self.api_key = api_key or os.getenv("GOLEAN_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it as GOLEAN_API_KEY environment variable or pass it to the constructor.")
        
        self.base_url = "https://prompt-compression-api.golean.ai"
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def compress_with_context(self, context: str, compression_mode: Optional[Literal["high", "medium", "low"]]="medium") -> Dict[str, Any]:
        """
        Compresses a context string using the GoLean API and calculates token statistics.

        Args:
            context (str): The input context string to be compressed.
            compression_mode (Optional[str]): Level of compression. Must be one of "high", "medium", or "low". High compression compresses prompt the most. Defaults to "medium".

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "compressed_result": The compressed context string.
                - "original_tokens": The number of tokens in the original context.
                - "compressed_tokens": The number of tokens in the compressed context.
                - "compression_rate": The ratio of compressed tokens to original tokens.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/compress_with_context/"
        payload = {"context": context, "compression_mode": compression_mode}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def compress_with_template(self, template: str, data: Dict[str, Any], compression_mode: Optional[Literal["high", "medium", "low"]]="medium") -> str:
        """
        Compresses a template string by replacing placeholders with compressed values and calculates token statistics.

        Args:
            template (str): A prompt template string with placeholders (e.g., "Summarize the following article: {article}.").
            data (dict): A dictionary where keys match the placeholders in the template, and values are strings to be compressed.
            compression_mode (Optional[str]): Level of compression. Must be one of "high", "medium", or "low". High compression compresses prompt the most. Defaults to "medium".

        Returns:
            Dict[str, Any]: A dictionary containing:
                - "compressed_result": The populated template with compressed values.
                - "original_tokens": The number of tokens in the original populated template.
                - "compressed_tokens": The number of tokens in the compressed populated template.
                - "compression_rate": The ratio of compressed tokens to original tokens.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
        """
        url = f"{self.base_url}/compress_with_template/"
        payload = {"template": template, "data": data, "compression_mode": compression_mode}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
