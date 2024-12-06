import re
from urllib.parse import urlparse
import requests
from typing import Dict, Any
from airosentris import Config


def is_valid_url(url: str) -> bool:
    """Validate the URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_token(token: str) -> bool:
    """Validate the token format as a UUID."""
    # Regular expression to match a UUID
    uuid_regex = re.compile(r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$')
    return bool(uuid_regex.match(token))


def login(token: str, url: str = "https://api.airosentris.com") -> Dict[str, Any]:
    """
    Login and initialize the pdamcc package with necessary configurations.

    Parameters:
    url (str): The API base URL.
    token (str): The authentication token.

    Raises:
    ValueError: If 'url' or 'token' is not valid.
    requests.exceptions.RequestException: If the request to the server fails.
    Exception: For other failures like unsuccessful login.

    Returns:
    Dict[str, Any]: A dictionary containing 'api_url', 'api_token', and 'agent_details'.
    """

    if not is_valid_url(url):
        raise ValueError("Invalid URL format.")

    if not is_valid_token(token):
        raise ValueError("Invalid token format.")

    Config.API_URL = url
    Config.API_TOKEN = token

    try:
        # Call the API to validate the user and token
        response = requests.post(
            f"{Config.API_URL}/api/v1/agent/login",
            json={"token": Config.API_TOKEN}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to server: {e}")

    result = response.json()
    if result.get('success'):
        Config.AGENT_DETAILS = result.get('data', {})
        user = Config.AGENT_DETAILS.get('user', {})
        user_name = user.get('name', 'Unknown User')
        print(f"airosentris initialized with URL: {Config.API_URL}, Token: {Config.API_TOKEN}, User: {user_name}")
    else:
        raise Exception(result.get('message', 'Login failed.'))
    
    # Call the API to get MINIO Config
    try:
        response = requests.get(
            f"{Config.API_URL}/api/v1/minio/config",
            headers={"Authorization": f"Bearer {Config.API_TOKEN}"}
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to server: {e}")
    
    result = response.json()
    if result.get('success'):
        minio_config = result.get('data', {})
        Config.MINIO_ACCESS_KEY = minio_config.get('access_key', '')
        Config.MINIO_SECRET_KEY = minio_config.get('secret_key', '')
        Config.MINIO_REGION = minio_config.get('region', '')
        Config.MINIO_BUCKET = minio_config.get('bucket', '')
        Config.MINIO_ENDPOINT = minio_config.get('endpoint', '')
        print(f"MINIO Config: {Config.MINIO_ACCESS_KEY}, {Config.MINIO_SECRET_KEY}, {Config.MINIO_REGION}, {Config.MINIO_BUCKET}, {Config.MINIO_ENDPOINT}")
    else:
        raise Exception(result.get('message', 'Failed to get MINIO Config.'))


def get_agent() -> str:
    return Config.AGENT_DETAILS
