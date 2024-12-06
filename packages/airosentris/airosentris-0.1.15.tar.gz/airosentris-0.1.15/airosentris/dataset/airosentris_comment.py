import os
import pickle
import json
import shutil

from airosentris import Config
from airosentris.utils.file_utils import ensure_dir
from airosentris.utils.network_utils import fetch_data


CACHE_DIR = "cache/airosentris"
API_PATH = "api/v1/run/dataset/download/{dataset_id}"


def load_data(dataset_id, cache_data=False):
    """
    Load data from the API or cache.

    Args:
        dataset_id (str): The ID of the dataset to load.
        cache_data (bool): Whether to cache the data locally.

    Returns:
        dict: The loaded dataset.

    Raises:
        ValueError: If the API_URL or API_TOKEN is not set, or if the API request fails.
    """
    # Construct the URL for the API request
    endpoint = f"{API_PATH}".format(dataset_id=dataset_id)

    # Handle caching
    cache_file = os.path.join(CACHE_DIR, f"{dataset_id}.pkl")
    if cache_data and os.path.exists(cache_file):
        try:
            with open(cache_file, "rb") as f:
                cached_data = pickle.load(f)
                return cached_data
        except Exception as e:
            print(f"Error loading cache: {e}. Fetching fresh data...")

    try:
        response = fetch_data(endpoint=endpoint)
    except Exception as e:
        raise ValueError(f"Failed to fetch data from API: {e}")

    data = response

    if cache_data:
        ensure_dir(CACHE_DIR)
        try:
            with open(cache_file, "wb") as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"Failed to cache data: {e}")

    return data
