import json
import logging
import os
import time
from threading import Thread
from airosentris.algorithm.BERT.BERTRunner import BERTRunner
from airosentris.client.APIClient import APIClient
from airosentris.message.Comment import Comment
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent
from airosentris.client.RabbitMQClient import RabbitMQClient
from airosentris.runner.RunnerRegistry import RunnerRegistry
from airosentris.runner.RunnerFactory import RunnerFactory
from minio import Minio
import tempfile


class Runner:
    def __init__(self):        
        self.rabbitmq_client = None
        self.evaluation_queue = "airosentris.evaluate.sentiment.queue" # change soon
        self.evaluation_thread = None
        self.scopes = ["complaint_category", "sentiment", "statement_type"]
        self.runners = {}
        self.runner_cache = {}
        self.api_client = APIClient()

    def setup_rabbitmq_client(self):
        """Initialize RabbitMQ client."""
        config = get_config()
        self.rabbitmq_client = RabbitMQClient(config=config)
        self.rabbitmq_client.connect()
        logging.info("RabbitMQ client initialized successfully.")

    def initialize_evaluation_queue(self):
        """Declare the evaluation queue."""
        if not self.rabbitmq_client:
            self.setup_rabbitmq_client()
        self.rabbitmq_client.declare_queue(self.evaluation_queue, durable=True)
        logging.info(f"Evaluation queue initialized: {self.evaluation_queue}")

    def start_listening(self):
        """Listen to incoming messages for evaluation."""
        while True:
            try:
                self.initialize_evaluation_queue()
                self.rabbitmq_client.consume_messages(
                    self.evaluation_queue,
                    self._process_incoming_message,
                )
                logging.info(f"[*] Waiting for messages in {self.evaluation_queue}. To exit press CTRL+C")
            except Exception as e:
                logging.error(f"Error in start_listening: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)

    def _process_incoming_message(self, ch, method, properties, body):
        """Process incoming RabbitMQ message."""
        try:
            message_data = json.loads(body)
            message = Comment(
                id=message_data.get("id"),
                timestamp=message_data.get("timestamp"),
                content=message_data.get("content"),
            )
            self.process_evaluation_message(message)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON message: {e}")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def process_evaluation_message(self, message: Comment):
        """Spawn threads to evaluate the message across all scopes."""
        threads = [
            Thread(target=self.evaluate, args=(message, scope))
            for scope in self.scopes
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def evaluate(self, message: Comment, scope_code: str):
        """Evaluate the message for a specific scope using the appropriate runner."""
        try:
            runner = self.runners.get(scope_code)
            if not runner:
                logging.warning(f"No runner found for scope: {scope_code}")
                return
            result = runner.evaluate(message)
            logging.info(f"Result for {scope_code}: {result}")
        except Exception as e:
            logging.error(f"Error evaluating {scope_code}: {e}")

    def get_active_model(self, scope_code: str):
        """Fetch active model details for a given scope."""
        try:
            response = self.api_client.post_data(
                endpoint="api/v1/ai-model/active/detail",
                data={"scope_code": scope_code},
            )
            if response.status_code == 200:
                return response.json().get("data")
            logging.error(f"Error retrieving active model for {scope_code}: {response.text}")
        except Exception as e:
            logging.error(f"Error fetching active model for {scope_code}: {e}")
        return None

    def download_model(self, run_id: str):
        """Download the model associated with a specific run_id."""
        try:
            import airosentris
            config = airosentris.Config
            minio_client = Minio(
                config.MINIO_ENDPOINT.replace("http://", "").replace("https://", ""),
                access_key=config.MINIO_ACCESS_KEY,
                secret_key=config.MINIO_SECRET_KEY,
                secure=False,
            )
            with tempfile.TemporaryDirectory() as tmp_dir:
                download_path = os.path.join(tmp_dir, f"{run_id}.zip")
                model_path = f"artifacts/models/{run_id}/"
                minio_client.fget_object(config.MINIO_BUCKET, f"model/{run_id}.zip", download_path)
                os.system(f"unzip -o {download_path} -d {model_path}")
                logging.info(f"Model downloaded for {run_id} at {model_path}")
                return model_path
        except Exception as e:
            logging.error(f"Error downloading model for {run_id}: {e}")
        return None

    def update_model_for_scope(self, scope_code: str):
        """Update the model for a given scope by fetching, downloading, and loading it."""
        active_model = self.get_active_model(scope_code)
        if not active_model:
            logging.warning(f"No active model found for {scope_code}")
            return

        run_id = active_model.get("run_id")
        if run_id and (scope_code not in self.runner_cache or self.runner_cache[scope_code] != run_id):
            model_path = self.download_model(run_id)
            if model_path:
                runner_class = RunnerFactory.get_runner(active_model["algorithm_code"])
                runner_instance = runner_class()
                runner_instance.load_model(scope_code, model_path)
                self.runners[scope_code] = runner_instance
                self.runner_cache[scope_code] = run_id
        else:
            logging.info(f"Model for {scope_code} is already up-to-date.")

    def auto_update_models(self):
        """Periodically update models for all scopes."""
        while True:
            for scope in self.scopes:
                self.update_model_for_scope(scope)
            logging.info("Models updated successfully.")
            time.sleep(300)

    def start_auto_update(self):
        """Start a thread for automatic model updates."""
        Thread(target=self.auto_update_models, daemon=True).start()

    def start_message_listener(self):
        """Start a thread for evaluation listener."""
        Thread(target=self.start_listening, daemon=True).start()

    def start(self):
        """Start all runner processes."""
        self.start_auto_update()
        time.sleep(120)
        self.start_message_listener()
