import requests
from typing import Optional, Dict, Any

class GreenscaleAI:
    """
    Python SDK for interacting with the Greenscale AI scraping API.
    """
    def __init__(self, api_key: str = "gs_scrape_free_trial", base_url: str = "https://scrape.greenscale.ai/"):
        """
        Initialize the SDK with an API key and an optional base URL.

        :param api_key: Your Greenscale AI API key.
        :param base_url: Base URL for the API (default: https://scrape.greenscale.ai/).
        """
        self.api_key = api_key
        self.base_url = base_url

    def scrape_url(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Send a scraping request to the Greenscale AI API.

        :param url: The URL to scrape.
        :param params: A dictionary of optional parameters (e.g., formats, include_metadata).
        :return: The API response as a dictionary or raises an error for failed requests.
        """
        endpoint = self.base_url
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        
        # Set default params if none are provided
        if params is None:
            params = {"formats": ["markdown"]}
        
        payload = {"url": url}
        payload.update(params)

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error {response.status_code}: {response.text}")