import os
import pickle
import json
import shutil

from airosentris import Config
from airosentris.utils.file_utils import ensure_dir
from airosentris.utils.network_utils import fetch_data

CACHE_DIR = "cache/social"


def load_data(scope, cache_data=False):
    """
    Loads the Comments dataset based on the specified scope by performing an HTTP GET request.

    Parameters:
    scope (str): The scope of the data to load. Can be one of 'sentiment', 'statement_type', or 'complaint_category'.
    cache_data (bool): If True, caches the loaded data to a file on disk. Default is False.

    Returns:
    dict: The data loaded from the HTTP GET request or cache.

    Raises:
    ValueError: If an invalid scope is provided or the API request is not successful.
    """
    # Validate the scope parameter to ensure it is one of the allowed values
    if scope not in ['sentiment', 'statement_type', 'complaint_category']:
        raise ValueError("Invalid scope provided")

    # Ensure API_URL and API_TOKEN are set
    if not Config.API_URL or not Config.API_TOKEN:
        raise ValueError("API_URL or API_TOKEN is not set. Please initialize the pdamcc package with valid config.")

    # Define the cache file path
    if cache_data:
        ensure_dir(CACHE_DIR)
        cache_file_path = os.path.join(CACHE_DIR, f"{scope}_data.pkl")

        # Check if cached data exists
        if os.path.exists(cache_file_path):
            with open(cache_file_path, 'rb') as file:
                data = pickle.load(file)
            return data

    # Construct the URL with the specific path based on the scope
    url = f"{Config.API_URL}/{scope}"

    # Fetch the data using the network utility
    response = fetch_data(url, Config.API_TOKEN)
    res = json.loads(response)

    # Check if the request was successful
    if not res.get('success', False):
        raise ValueError("Failed to load data: API request was not successful")

    data = res.get('data')

    # If cache_data is True, save the data to a pickle file in the cache directory
    if cache_data:
        with open(cache_file_path, 'wb') as file:
            pickle.dump(data, file)

    return data


def clear_cache():
    """
    Clears the cache directory.
    """
    if os.path.exists(CACHE_DIR):
        shutil.rmtree(CACHE_DIR)
        print("Cache cleared.")
    else:
        print("Cache directory does not exist.")
