import pika
import json
import time
import logging
from threading import Thread
from airosentris.agent.Agent import Agent
from airosentris.hardware.SystemInfo import SystemInfo
from airosentris.message.AgentStatus import AgentStatusRequest
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent


class Crawler:
    def __init__(self):
        self.agent = get_agent()
        self.on_new_message = self.crawling_callback

    def _connect(self, config: dict) -> tuple:
        try:
            credentials = pika.PlainCredentials(config['username'], config['password'])
            parameters = pika.ConnectionParameters(
                host=config['host'],
                port=int(config['port']),
                virtual_host=config['vhost'],
                credentials=credentials
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"AMQP Connection error: {e}")
            raise
        except pika.exceptions.ProbableAuthenticationError as e:
            logging.error(f"Authentication error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during connection: {e}")
            raise

    def provide_query(self) -> None:
        if self.on_request_agent_info is None:
            raise ValueError("on_request_agent_info callback must be provided and must be callable")

        while True:
            try:
                config = get_config()
                connection, channel = self._connect(config)

                channel.exchange_declare(exchange='airosentris.agent', exchange_type='fanout', durable=True)

                queue_result = channel.queue_declare(queue=self.agent_query_queue, auto_delete=True, durable=False)
                queue_name = queue_result.method.queue

                channel.queue_bind(exchange='airosentris.agent', queue=queue_name)

                def on_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        message_receive = AgentStatusRequest(
                            code=message.get("code")
                        )
                        self.on_request_agent_info(message_receive)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                channel.basic_consume(queue=self.agent_query_queue, on_message_callback=on_message, auto_ack=True)
                logging.info(f"[*] Waiting for messages in {self.agent_query_queue}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in provide_query method: {e}")
                break

    def watch(self):
        if self.on_new_message is None:
            raise ValueError("on_new_message callback must be provided and must be callable")

        while True:
            try:
                queue_name = None
                config = get_config()
                logging.info(f"RabbitMQ Configuration: {config}")
                connection, channel = self._connect(config)
                channel.queue_declare(queue=queue_name, durable=True)

                def on_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        message_receive = None
                        self.on_new_message(message_receive)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
                # logging.info(f"[*] Waiting for messages in {scope}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in watch method: {e}")
                break

    def crawling_callback(self):
        pass

    def start_crawling_thread(self):
        pass

    def start(self):
        self.start_crawling_thread()

    