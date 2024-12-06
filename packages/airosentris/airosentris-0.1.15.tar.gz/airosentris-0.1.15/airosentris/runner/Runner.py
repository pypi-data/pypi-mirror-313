import pika
import json
import time
import logging
from threading import Thread
from airosentris.algorithm.BERT.BERTRunner import BERTRunner
from airosentris.hardware.SystemInfo import SystemInfo
from airosentris.message.AgentStatus import AgentStatusRequest
from airosentris.message.Comment import Comment
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent


class Runner:

    def __init__(self):
        self.agent = get_agent()
        self.agent_query_queue = 'airosentris.agent-{}'.format(str(self.agent['id']))
        self.on_new_message = self.evaluate_callback
        self.agent_thread = None
        self.evaluate_thread = None
        self.runner = BERTRunner()

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

    def watch(self, scope: str = 'sentiment') -> None:
        if self.on_new_message is None:
            raise ValueError("on_new_message callback must be provided and must be callable")

        while True:
            try:
                queue_name = "airosentris.evaluate." + scope + ".queue"
                config = get_config()
                logging.info(f"RabbitMQ Configuration: {config}")
                connection, channel = self._connect(config)
                channel.queue_declare(queue=queue_name, durable=True)

                def on_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        message_receive = Comment(
                            id=message.get("id"),
                            timestamp=message.get("timestamp"),
                            content=message.get("content")
                        )
                        self.on_new_message(message_receive)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                channel.basic_consume(queue=queue_name, on_message_callback=on_message, auto_ack=True)
                logging.info(f"[*] Waiting for messages in {scope}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in watch method: {e}")
                break

    def evaluate_callback(self, message_receive: Comment) -> None:
        logging.info(f"Processed message: {message_receive}")
        message_id = message_receive.id
        message_content = message_receive.content    
        result = self.runner.evaluate(message_id, message_content)
        
        return result   

    def start_evaluate_thread(self, scope: str = 'sentiment'):
        self.evaluate_thread = Thread(target=self.watch, args=(scope,))
        self.evaluate_thread.start()

    def start(self):
        self.runner.auto_update()
        self.start_evaluate_thread()        
