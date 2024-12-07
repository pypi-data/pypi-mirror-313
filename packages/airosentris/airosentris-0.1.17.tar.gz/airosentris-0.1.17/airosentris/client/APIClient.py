import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from airosentris import Config

class APIClient:
    """A reusable API client for interacting with the main application."""
    
    def __init__(self):
        if not Config.API_URL or not Config.API_TOKEN:
            raise ValueError("API_URL or API_TOKEN is not set. Please initialize the airosentris package with valid config.")
        
        self.api_url = Config.API_URL
        self.api_token = Config.API_TOKEN
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        self._setup_session()
    
    def _setup_session(self):
        """Set up the session with retries and logging."""
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.logger.info("Session configured with retry logic.")
    
    def _build_url(self, endpoint):
        """Construct the full URL for the API endpoint."""
        return f"{self.api_url}/{endpoint}"
    
    def _build_headers(self):
        """Build the headers for API requests."""
        return {'Authorization': f"Bearer {self.api_token}"}
    
    def fetch_data(self, endpoint, timeout=10):
        """Fetch data from the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()
        
        try:
            self.logger.info(f"Fetching data from {url}")
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses
            response_data = response.json()
            
            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"Error fetching data: {error_message}")
                raise Exception(error_message)
            
            self.logger.info("Data fetched successfully.")
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def post_data(self, endpoint, data, files=None, timeout=10):
        """Post data to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()
        
        try:
            self.logger.info(f"Posting data to {url} with payload: {data}")
            response = self.session.post(url, headers=headers, data=data, files=files, timeout=timeout)
            response.raise_for_status()  # Raise HTTPError for bad responses
            response_data = response.json()
            
            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"Error posting data: {error_message}")
                raise Exception(error_message)
            
            self.logger.info("Data posted successfully.")
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def delete_data(self, endpoint, timeout=10):
        """Send a DELETE request to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()
        
        try:
            self.logger.info(f"Deleting data at {url}")
            response = self.session.delete(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()
            
            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"Error deleting data: {error_message}")
                raise Exception(error_message)
            
            self.logger.info("Data deleted successfully.")
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
    
    def put_data(self, endpoint, data, timeout=10):
        """Send a PUT request to the specified API endpoint."""
        url = self._build_url(endpoint)
        headers = self._build_headers()
        
        try:
            self.logger.info(f"Updating data at {url} with payload: {data}")
            response = self.session.put(url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            response_data = response.json()
            
            if not response_data.get("success", True):
                error_message = response_data.get("message", "Unknown error")
                self.logger.error(f"Error updating data: {error_message}")
                raise Exception(error_message)
            
            self.logger.info("Data updated successfully.")
            return response
        except requests.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise
