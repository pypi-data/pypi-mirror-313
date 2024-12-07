import json
import logging
import time
from threading import Thread
from airosentris.algorithm.BERT.BERTRunner import BERTRunner
from airosentris.message.Comment import Comment
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent
from airosentris.client.RabbitMQClient import RabbitMQClient


class EvaluationRunner:
    def __init__(self):        
        self.bert_runner = BERTRunner()
        self.rabbitmq_client = None
        self.evaluation_queue = "airosentris.evaluate.queue"
        self.evaluation_thread = None

    def setup_rabbitmq_client(self):
        """Menginisialisasi koneksi RabbitMQ melalui RabbitMQClient."""
        config = get_config()
        self.rabbitmq_client = RabbitMQClient(config=config)
        self.rabbitmq_client.connect()
        logging.info("RabbitMQ client initialized successfully.")

    def start_listening(self):
        """Mendengarkan pesan baru untuk proses evaluasi."""
        while True:
            try:
                logging.info(f"Setting up RabbitMQ listener for queue: {self.evaluation_queue}")
                self.rabbitmq_client.declare_queue(self.evaluation_queue, durable=True)

                def on_message(body):
                    try:
                        # Parsing pesan dan memprosesnya
                        message = json.loads(body)
                        message_receive = Comment(
                            id=message.get("id"),
                            timestamp=message.get("timestamp"),
                            content=message.get("content")
                        )
                        self.process_evaluation_message(message_receive)
                    except json.JSONDecodeError as e:
                        logging.error(f"Failed to parse JSON message: {e}")
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                # Mendengarkan pesan menggunakan callback
                self.rabbitmq_client.consume_messages(self.evaluation_queue, on_message)
                logging.info(f"[*] Waiting for messages in {self.evaluation_queue}. To exit press CTRL+C")                

            except Exception as e:
                logging.error(f"Error in start_listening: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)

    def process_evaluation_message(self, message_receive: Comment) -> None:
        """Callback untuk memproses pesan evaluasi."""
        logging.info(f"Processing message: {message_receive}")
        message_id = message_receive.id
        message_content = message_receive.content
        result = self.bert_runner.evaluate(message_id, message_content)
        logging.info(f"Evaluation result for message ID {message_id}: {result}")

    def launch_evaluation_listener(self):
        """Memulai thread untuk mendengarkan pesan evaluasi."""
        self.evaluation_thread = Thread(target=self.start_listening)
        self.evaluation_thread.start()

    def start(self):
        """Memulai seluruh proses runner."""
        self.setup_rabbitmq_client()
        self.bert_runner.auto_update()
        self.launch_evaluation_listener()
