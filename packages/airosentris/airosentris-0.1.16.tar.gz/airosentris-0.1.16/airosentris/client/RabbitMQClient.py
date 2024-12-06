import time
import pika
import logging
import json


class RabbitMQClient:
    def __init__(self, config=None, heartbeat=60, blocked_connection_timeout=300):
        self.host=config['host']
        self.port=int(config['port'])
        self.username=config['username']
        self.password=config['password']
        self.vhost=config['vhost']
        self.heartbeat = heartbeat
        self.blocked_connection_timeout = blocked_connection_timeout
        self.connection = None
        self.channel = None

    def connect(self, max_retries=5, backoff_factor=2):
        retries = 0
        while retries < max_retries:
            try:
                logging.info("Establishing connection to RabbitMQ...")
                credentials = pika.PlainCredentials(self.username, self.password)
                parameters = pika.ConnectionParameters(
                    host=self.host,
                    port=self.port,
                    virtual_host=self.vhost,
                    credentials=credentials,
                    heartbeat=self.heartbeat,
                    blocked_connection_timeout=self.blocked_connection_timeout
                )
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                logging.info("Connection to RabbitMQ established successfully.")
                return
            except pika.exceptions.AMQPConnectionError as e:
                retries += 1
                delay = backoff_factor ** retries
                logging.error(f"RabbitMQ connection error: {e}")
                time.sleep(delay)
            except pika.exceptions.ProbableAuthenticationError as e:
                logging.error(f"Authentication error: {e}")
                raise
            except Exception as e:
                retries += 1
                delay = backoff_factor ** retries
                logging.error(f"Unexpected error while connecting to RabbitMQ: {e}")
                time.sleep(delay)

        raise ConnectionError("Failed to connect to RabbitMQ after maximum retries.")

    def close(self):
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        logging.info("RabbitMQ connection closed.")

    def declare_exchange(self, exchange_name, exchange_type='direct', durable=True):
        try:
            self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)
            logging.info(f"Exchange '{exchange_name}' declared successfully.")
        except Exception as e:
            logging.error(f"Error declaring exchange '{exchange_name}': {e}")
            raise

    def declare_queue(self, queue_name, durable=True, auto_delete=False):
        try:
            self.channel.queue_declare(queue=queue_name, durable=durable, auto_delete=auto_delete)
            logging.info(f"Queue '{queue_name}' declared successfully.")
        except Exception as e:
            logging.error(f"Error declaring queue '{queue_name}': {e}")
            raise

    def bind_queue(self, exchange_name, queue_name, routing_key):
        try:
            self.channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
            logging.info(f"Queue '{queue_name}' bound to exchange '{exchange_name}' with routing key '{routing_key}'.")
        except Exception as e:
            logging.error(f"Error binding queue '{queue_name}' to exchange '{exchange_name}': {e}")
            raise

    def publish_message(self, exchange_name, routing_key, message):
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            self.channel.basic_publish(
                exchange=exchange_name,
                routing_key=routing_key,
                body=message
            )
            logging.info(f"Message published to exchange '{exchange_name}' with routing key '{routing_key}'.")
        except Exception as e:
            logging.error(f"Error publishing message: {e}")
            raise

    def consume_messages(self, queue_name, on_message_callback, auto_ack=True):
        try:
            logging.info(f"[*] Waiting for messages in queue '{queue_name}'. To exit, press CTRL+C.")
            self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=auto_ack)
            self.channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"Connection error during message consumption: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during message consumption: {e}")
            raise

    def stop_consuming(self):
        if self.channel and self.channel.is_open:
            self.channel.stop_consuming()
            logging.info("Stopped consuming messages.")


