import time
from abc import ABC, abstractmethod
import pika
import logging

from airosentris import Config
from airosentris.config.ConfigFetcher import get_config


class BaseTrainer(ABC):

    def __init__(self):
        self.rabbitmq_config = get_config()
        self.rabbitmq_connection = None
        self.rabbitmq_channel = None

    @abstractmethod
    def train(self, data, labels):
        pass

    @abstractmethod
    def evaluate(self, test_data, test_labels):
        pass

    @abstractmethod
    def save_model(self, file_path):
        pass

    @abstractmethod
    def load_model(self, file_path):
        pass

    def _connect(self, config: dict, max_retries=5, backoff_factor=2):
        """
        Establishes a connection to RabbitMQ with auto-reconnect.

        Args:
            config (dict): RabbitMQ connection parameters.
            max_retries (int): Maximum number of retry attempts.
            backoff_factor (int): Backoff multiplier for exponential delay.
        """
        retries = 0
        while retries < max_retries:
            try:
                credentials = pika.PlainCredentials(config['username'], config['password'])
                parameters = pika.ConnectionParameters(
                    host=config['host'],
                    port=int(config['port']),
                    virtual_host=config['vhost'],
                    credentials=credentials,
                    heartbeat=600,  # Extend heartbeat to 10 minutes
                    blocked_connection_timeout=300  # Prevent timeout errors
                )
                self.rabbitmq_connection = pika.BlockingConnection(parameters)
                self.rabbitmq_channel = self.rabbitmq_connection.channel()
                logging.info("Successfully connected to RabbitMQ.")
                return
            except pika.exceptions.AMQPConnectionError as e:
                retries += 1
                delay = backoff_factor ** retries
                logging.warning(f"Connection failed ({retries}/{max_retries}). Retrying in {delay} seconds. Error: {e}")
                time.sleep(delay)
            except pika.exceptions.ProbableAuthenticationError as e:
                logging.error(f"Authentication error: {e}")
                raise
            except Exception as e:
                retries += 1
                delay = backoff_factor ** retries
                logging.error(f"Unexpected error during connection ({retries}/{max_retries}): {e}")
                time.sleep(delay)

        raise ConnectionError("Failed to connect to RabbitMQ after maximum retries.")