import json
import os
import requests
import airosentris as air

from dotenv import load_dotenv
load_dotenv()


class HttpRequestCrawlerCIS:

    def __init__(self):
        self.cis_url = os.getenv("CIS_URL")
        self.cis_header_from = os.getenv("CIS_HEADER_FROM")
        self.cis_token = os.getenv("CIS_HEADER_X_APIKEY")   

        self.headers = {
            "x-api-key": f"{self.cis_token}",
            "from": self.cis_header_from
        }

        config = air.get_config()

        self.api_url = config.API_URL
        self.api_token = config.API_TOKEN

        self.api_header = {
            "Authorization": f"Bearer {self.api_token}",
            "X-CSRF-TOKEN": ""
        }

    def get_cis_comments(self, start=0, limit=10):
        params = {
            "start": start,
            "limit": limit
        }
        try:
            response = requests.get(self.cis_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return None

    def get_last_sequence(self):
        url = f"{self.api_url}/api/v1/comment/get/cis/last-sequence"
        try:
            response = requests.get(url, headers=self.api_header)
            response_data = response.json()

            if response_data.get("success"):
                return response_data["data"].get("sequence", 0)
            else:
                print(f"Failed to retrieve last sequence: {response_data.get('message')}")
                return None
        except Exception as err:
            print(f"An error occurred: {err}")
        return None
    
    def post_comments(self, data):                   
        url = f"{self.api_url}/api/v1/comment/upsert/cis"
        payload = {"data": data}
        try:
            response = requests.post(url, headers=self.api_header, json=payload)
            response_data = response.json()

            if response_data.get("success"):
                print("Comments " + json.dumps(data) + " post successfully.")
            else:
                print(f"Failed to post comments: {response_data.get('message')}")
        except Exception as err:
            print(f"An error occurred: {err}")

        return None