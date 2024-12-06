import requests
import json
from pprint import pprint

class DesyncSearch:
    def __init__(self, api_key: str, base_url: str = "https://vpnfv7czdzl54idmrn7rncmb7e0ljfbv.lambda-url.us-east-1.on.aws/"):
        """
        Initialize the client with an API key and optional base URL.
        """
        self.api_key = api_key
        self.base_url = base_url

    def search(self, scrape_url: str, stealth_level: int = 1, extract_text_content: bool = True, remove_link_duplicates: bool = True):
        """
        Perform a search using the API.

        Args:
            scrape_url (str): The URL to scrape.
            stealth_level (int): The stealth level for the scraper (default: 1).
            extract_text_content (bool): Whether to extract text content (default: True).
            remove_link_duplicates (bool): Whether to remove duplicate links (default: True).

        Returns:
            DesyncSearchResponse: Parsed response object.
        """
        if isinstance(scrape_url, list):
            return self.bulk_search(scrape_url, stealth_level, extract_text_content, remove_link_duplicates)

        payload = {
            "operation": "single_search",
            "SCRAPE_URL": scrape_url,
            "stealth_level": stealth_level,
            "api_key": self.api_key,
            "extract_text_content": extract_text_content,
            "remove_link_duplicates": remove_link_duplicates
        }

        try:
            print(f"Sending request to API with payload: {json.dumps(payload)}")
            response = requests.post(self.base_url, json=payload)
            #print(f"Received response status: {response.status_code}")
            #print(f"Response headers: {response.headers}")
            #print(f"Response content: {response.text}")
            response.raise_for_status()
            response_json = response.json()
            if 'body' in response_json:
                # Parse the 'body' field, which is a JSON string
                body = json.loads(response_json.get('body', '{}'))
                return DesyncSearchResponse(body)
            else:
                return DesyncSearchResponse(response_json)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to perform search: {str(e)}")

    def bulk_search(self, links: list, stealth_level: int = 1, extract_text_content: bool = True, remove_link_duplicates: bool = True):
        """
        Initiate a bulk search using the API. This method starts an asynchronous
        search via the state machine and informs the user when it starts.

        Args:
            links (list): List of URLs to scrape.
            stealth_level (int): The stealth level for the scraper (default: 1).
            extract_text_content (bool): Whether to extract text content (default: True).
            remove_link_duplicates (bool): Whether to remove duplicate links (default: True).

        Returns:
            DesyncBulkSearchResponse: Parsed bulk search response object.
        """
        payload = {
            "operation": "bulk_search",
            "links": links,
            "stealth_level": stealth_level,
            "api_key": self.api_key,
            "extract_text_content": extract_text_content,
            "remove_link_duplicates": remove_link_duplicates
        }

        try:
            print(f"Sending bulk search request to API with payload: {json.dumps(payload)}")
            response = requests.post(self.base_url, json=payload)
            #print(f"Received response status: {response.status_code}")
            #print(f"Response headers: {response.headers}")
            #print(f"Response content: {response.text}")
            response.raise_for_status()
            response_json = response.json()
            if 'body' in response_json:
                # Parse the 'body' field, which is a JSON string
                body = json.loads(response_json.get('body', '{}'))
                return DesyncBulkSearchResponse(body)
            else:
                return DesyncBulkSearchResponse(response_json)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to perform bulk search: {str(e)}")

    def get_response_data(self, response):
        """
        Pretty print the response data.

        Args:
            response: DesyncSearchResponse or DesyncBulkSearchResponse object.
        """
        if isinstance(response, DesyncSearchResponse):
            print("Single Search Response:")
            pprint({
                "text_content": response.text_content,
                "internal_links": response.internal_links,
                "external_links": response.external_links,
            })
        elif isinstance(response, DesyncBulkSearchResponse):
            print("Bulk Search Response:")
            pprint({
                "executionArn": response.executionArn,
                "message": response.message,
            })
        else:
            print("Unknown response type.")

class DesyncSearchResponse:
    def __init__(self, response_data):
        # Access the 'scraping_result' key
        scraping_result = response_data.get("scraping_result", {})
        self.text_content = scraping_result.get("text_content", "")
        self.internal_links = scraping_result.get("internal_links", [])
        self.external_links = scraping_result.get("external_links", [])
        self.scrape_url = scraping_result.get("SCRAPE_URL", "")

        # Optionally, store 'db_insertion_response' if needed
        self.db_insertion_response = response_data.get("db_insertion_response", {})

    def __repr__(self):
        return f"<DesyncSearchResponse(text_content_length={len(self.text_content)}, internal_links={len(self.internal_links)}, external_links={len(self.external_links)})>"

class DesyncBulkSearchResponse:
    def __init__(self, response_data):
        self.executionArn = response_data.get("executionArn", "")
        self.message = response_data.get("message", "")

    def __repr__(self):
        return f"<DesyncBulkSearchResponse(executionArn='{self.executionArn}', message='{self.message}')>"
