import os
import time
from abc import ABC, abstractmethod
import pika
import logging

from airosentris import Config
from airosentris.client.APIClient import APIClient
from airosentris.config.ConfigFetcher import get_config
from airosentris.message.Comment import Comment


class BaseRunner(ABC):

    def __init__(self):
        self.rabbitmq_config = get_config()
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None
        self.api_client = APIClient()
        
    @abstractmethod
    def evaluate(self, comment: Comment):
        pass

    @abstractmethod
    def load_model(self, scope_code, model_path):
        pass

    def send_tag_to_api(self, comment_id, scope_code, scope_label_code):
        """ Method to send the tag to the API """

        endpoint = "api/v1/comment/tag/agent"        

        payload = {
            "comment_id": comment_id,
            "scopes_code": scope_code,
            "scopes_label_code": scope_label_code
        }

        try:
            response = self.api_client.post_data(endpoint=endpoint, data=payload)
            if response.status_code == 200:
                logging.info(f"Successfully tagged comment {comment_id} with {scope_code}: {scope_label_code}")
            else:
                logging.error(f"Failed to tag comment {comment_id} with {scope_code}: {scope_label_code}, Response: {response.text}")
        except Exception as e:
            logging.error(f"Error sending tag to API: {e}")