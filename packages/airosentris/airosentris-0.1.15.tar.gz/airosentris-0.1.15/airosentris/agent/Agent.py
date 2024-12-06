import requests
from airosentris import Config


class Agent:
    @staticmethod
    def register(config):
        """
        Register an agent by asking the user to enter their username and password.

        Parameters:
        config (dict): A dictionary containing configuration keys 'url'.

        Raises:
        ValueError: If 'url' is not provided in the config.

        Returns:
        dict: A dictionary containing 'api_url', 'api_token', and 'agent_details'.
        """
        if 'url' not in config:
            raise ValueError("Config must include 'url'.")

        Config.API_URL = config['url']

        # Ask the user to enter their username and password
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Call the API to register the agent
        response = requests.post(
            f"{Config.API_URL}/register",
            json={"username": username, "password": password}
        )

        if response.status_code == 200:
            response_data = response.json()
            Config.API_TOKEN = response_data['token']
            Config.AGENT_DETAILS = response_data['agent_details']
            print(
                f"Agent registered with URL: {Config.API_URL}, Token: {Config.API_TOKEN}, and Agent Details: {Config.AGENT_DETAILS}")
            return {
                'api_url': Config.API_URL,
                'api_token': Config.API_TOKEN,
                'agent_details': Config.AGENT_DETAILS
            }
        else:
            raise Exception("Failed to register agent with the server.")

    @staticmethod
    def update(data):
        response = requests.post(
            f"{Config.API_URL}/api/v1/agent/update",
            headers={"Authorization": f"Bearer {Config.API_TOKEN}"},
            json=data
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update resource")

    @staticmethod
    def delete(resource_id):
        """
        Delete a resource.

        Parameters:
        resource_id (str): The ID of the resource to be deleted.

        Returns:
        dict: The details of the deleted resource.
        """
        response = requests.delete(
            f"{Config.API_URL}/delete/{resource_id}",
            headers={"Authorization": f"Bearer {Config.API_TOKEN}"}
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to delete resource with ID {resource_id}")
