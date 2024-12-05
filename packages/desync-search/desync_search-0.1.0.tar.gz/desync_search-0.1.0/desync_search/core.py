import requests
from pprint import pprint
import json


class DesyncSearch:
    def __init__(self, api_key: str, base_url: str = "https://vpnfv7czdzl54idmrn7rncmb7e0ljfbv.lambda-url.us-east-1.on.aws/"):
        """
        Initialize the client with an API key and optional base URL.
        """
        self.api_key = api_key
        self.base_url = base_url

    def search(self, scrape_url: str, stealth_level: int = 1):
        """
        Perform a search using the API.
        
        Args:
            scrape_url (str): The URL to scrape.
            stealth_level (int): The stealth level for the scraper (default: 1).
        
        Returns:
            DesyncSearchResponse: Parsed response object.
        """
        payload = {
            "SCRAPE_URL": scrape_url,
            "stealth_level": stealth_level,
            "api_key": self.api_key,
        }

        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return DesyncSearchResponse(response.json())
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to perform search: {str(e)}")

class DesyncSearchResponse:
    def __init__(self, response_data):
        """
        Initialize the response object with JSON data.
        """
        self.text_content = response_data.get("text_content", "")
        self.internal_links = response_data.get("internal_links", [])
        self.external_links = response_data.get("external_links", [])
