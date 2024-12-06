import json
import time
import pika
import logging
from threading import Lock
from datetime import datetime


class RabbitMQLogger:
    """
    Handles RabbitMQ connection, messaging, and logging using a Singleton pattern.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of RabbitMQLogger is created.
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(RabbitMQLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        """
        Initializes RabbitMQLogger with configuration. Ensures initialization happens only once.

        Args:
            config (dict): RabbitMQ connection configuration.
        """
        if not hasattr(self, "initialized"):
            self.config = config
            self.connection = None
            self.channel = None
            self.initialized = True

    def connect(self, max_retries=5, backoff_factor=2):
        """
        Establishes a connection to RabbitMQ with auto-reconnect.

        Args:
            max_retries (int): Maximum number of retry attempts.
            backoff_factor (int): Backoff multiplier for exponential delay.

        Raises:
            ConnectionError: If connection fails after max_retries.
        """
        retries = 0
        while retries < max_retries:
            try:
                credentials = pika.PlainCredentials(self.config['username'], self.config['password'])
                parameters = pika.ConnectionParameters(
                    host=self.config['host'],
                    port=int(self.config['port']),
                    virtual_host=self.config['vhost'],
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300,
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
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

    def publish_message(self, exchange, routing_key, message):
        """
        Publishes a message to a RabbitMQ exchange.

        Args:
            exchange (str): RabbitMQ exchange name.
            routing_key (str): Routing key.
            message (str): Message to publish.

        Raises:
            Exception: If message publishing fails.
        """
        try:
            if not self.channel or self.connection.is_closed:
                logging.info("RabbitMQ connection is closed. Reconnecting...")
                self.connect()
            self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
            logging.info(f"Published message to RabbitMQ: {message}")
        except pika.exceptions.AMQPChannelError as e:
            logging.error(f"Channel error while publishing message: {e}. Attempting to reconnect.")
            self.connect()
            self.publish_message(exchange, routing_key, message)  # Retry after reconnecting
        except Exception as e:
            logging.error(f"Failed to publish message to RabbitMQ: {e}")
            raise

    def log_command(self, project_id, run_id, message):
        """
        Logs a command message to RabbitMQ.

        Args:
            project_id (str): Project ID.
            run_id (str): Run ID.
            message (str): Command message.
        """
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message_data = {
            "project_id": project_id,
            "run_id": run_id,
            "type": "command",
            "time": current_time,
            "data": message
        }
        self.publish_message("airosentris.status", "", json.dumps(message_data))


    def log_metric(self, project_id, run_id, data):
        """
        Logs a command message to RabbitMQ.

        Args:
            project_id (str): Project ID.
            run_id (str): Run ID.
            data (obj): Data.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message_data = {
            "project_id": project_id,
            "run_id": run_id,
            "type": "metric",
            "time": current_time,
            "data": json.dumps(data)
        }
        self.publish_message("airosentris.status", "", json.dumps(message_data))

    def log_status(self, project_id, run_id, status):
        """
        Logs a status message to RabbitMQ.

        Args:
            project_id (str): Project ID.
            run_id (str): Run ID.
            status (str): Status message.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message_data = {
            "project_id": project_id,
            "run_id": run_id,
            "type": "status",
            "time": current_time,
            "data": status
        }
        self.publish_message("airosentris.status", "", json.dumps(message_data))