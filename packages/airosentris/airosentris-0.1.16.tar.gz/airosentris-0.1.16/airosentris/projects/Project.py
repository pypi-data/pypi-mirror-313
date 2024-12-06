import requests
import json
from typing import Optional, Dict, Any
from airosentris import Config


def login_required():
    """
    Ensures the user is logged in by checking if the API URL and Token are set.
    If not, raises an exception or prompts the user to log in.
    """
    if not Config.API_URL or not Config.API_TOKEN:
        raise Exception("You must log in before initializing a project.")


def init(
    project: str,
    name: Optional[str] = None,
    scope: str = 'sentiment',
    description: str = None,
    algorithm: str = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Initialize the pdamcc package with necessary project configurations and post to the server.

    Parameters:
    project (str): The name of the project.
    name (Optional[str]): The name of the run.
    scope (str): The scope of the project. Default is 'sentiment'.
    description (str): The description of the project.
    algorithm (str): The algorithm used in the project.
    config (Optional[Dict[str, Any]]): A dictionary containing additional configuration keys.

    Raises:
    ValueError: If any of the required parameters are not provided.
    Exception: If the user is not logged in or if the project initialization fails.

    Returns:
    Dict[str, Any]: A dictionary containing project details.
    """

    # Ensure user is logged in
    login_required()

    # Validate required parameters
    if not project or not description or not algorithm:
        raise ValueError("Project name, description, and algorithm must be provided.")

    Config.PROJECT_NAME = project
    Config.PROJECT_DESCRIPTION = description
    Config.PROJECT_ALGORITHM = algorithm
    Config.PROJECT_SCOPE = scope

    if config is None:
        # If config is None, prompt the user to login
        print("Config is None, you must log in first.")
        raise Exception("Please log in before initializing the project.")

    # Post the project details to the server
    try:
        response = requests.post(
            f"{Config.API_URL}/api/v1/project/init",
            headers={"Authorization": f"Bearer {Config.API_TOKEN}"},
            json={
                'project_name': Config.PROJECT_NAME,
                'project_description': Config.PROJECT_DESCRIPTION,
                'project_algorithm': Config.PROJECT_ALGORITHM,
                'project_scope': Config.PROJECT_SCOPE,
                'run_name': name,
                'run_config': json.dumps(config)
            }
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to initialize project on the server: {e}")

    result = response.json()
    if result.get('success'):
        print(f"Project initialized with Name: {Config.PROJECT_NAME}, Description: {Config.PROJECT_DESCRIPTION}, Algorithm: {Config.PROJECT_ALGORITHM}, Scope: {Config.PROJECT_SCOPE}")
        return {
            'project_name': Config.PROJECT_NAME,
            'project_description': Config.PROJECT_DESCRIPTION,
            'project_algorithm': Config.PROJECT_ALGORITHM,
            'project_scope': Config.PROJECT_SCOPE,
            'run_name': name
        }
    else:
        raise Exception(result.get('message', 'Failed to initialize project on the server.'))