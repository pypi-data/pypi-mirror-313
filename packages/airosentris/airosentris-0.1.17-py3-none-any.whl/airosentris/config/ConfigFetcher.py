import airosentris
import requests


def get_config():
    """
    Fetches the RabbitMQ configuration from the API using a Bearer token for authentication.

    Returns:
        dict: The configuration data.

    Raises:
        Exception: If the configuration retrieval fails.
    """
    try:
        config = airosentris.get_config()

        # Prepare the headers with the Bearer token for authentication
        headers = {
            'Authorization': f"Bearer {config.API_TOKEN}"
        }

        # Make a GET request to the API endpoint to fetch the RabbitMQ configuration
        response = requests.get(
            f"{config.API_URL}/api/v1/pubsub/config",
            headers=headers
        )

        response_data = response.json()

        if response.status_code != 200 or not response_data.get('success'):
            raise Exception(f"Failed to retrieve config: {response_data.get('message', 'Unknown error')}")

        return response_data['data']
    except Exception as e:
        print(f"Error fetching config: {e}")
        raise


class ConfigFetcher:
    pass