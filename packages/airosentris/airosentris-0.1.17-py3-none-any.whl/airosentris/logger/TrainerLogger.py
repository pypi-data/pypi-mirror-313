import json
import logging
from datetime import datetime
from threading import Lock
from airosentris.client.RabbitMQClient import RabbitMQClient
from airosentris.config.ConfigFetcher import get_config


class TrainerLogger:
    """
    Logger khusus untuk mencatat aktivitas pelatihan model ke RabbitMQ.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """
        Ensure only one instance of TrainerLogger is created.
        """
        if not cls._instance:
            with cls._lock:  # Thread-safe initialization
                if not cls._instance:  # Double-checked locking
                    cls._instance = super(TrainerLogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, config=None):
        """
        Ensures initialization happens only once.
        """
        if not hasattr(self, "initialized"):
            config = get_config()
            self.rabbitmq_client = RabbitMQClient(config=config)
            self.rabbitmq_client.connect()
            self.exchange_name = "airosentris.status"
            self.initialized = True
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
        self.logger.info("TrainerLogger initialized successfully.")
        # logging.info("TrainerLogger initialized successfully.")

    def _prepare_log_message(self, project_id: str, run_id: str, log_type: str, data: dict | str) -> str:
        """
        Membuat pesan log dalam format JSON.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            log_type (str): Jenis log (command, metric, atau status).
            data (dict | str): Data log.

        Returns:
            str: Pesan log dalam format JSON.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return json.dumps({
            "project_id": project_id,
            "run_id": run_id,
            "type": log_type,
            "time": current_time,
            "data": data if isinstance(data, str) else json.dumps(data)
        })

    def log_command(self, project_id: str, run_id: str, command: str) -> None:
        """
        Mencatat perintah pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            command (str): Perintah yang dijalankan.
        """
        message = self._prepare_log_message(project_id, run_id, "command", command)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"Command log sent: {message}")

    def log_metric(self, project_id: str, run_id: str, metrics: dict) -> None:
        """
        Mencatat metrik hasil pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            metrics (dict): Data metrik pelatihan.
        """
        message = self._prepare_log_message(project_id, run_id, "metric", metrics)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"Metric log sent: {message}")

    def log_status(self, project_id: str, run_id: str, status: str) -> None:
        """
        Mencatat status pelatihan.

        Args:
            project_id (str): ID proyek.
            run_id (str): ID pelatihan atau proses.
            status (str): Status pelatihan.
        """
        message = self._prepare_log_message(project_id, run_id, "status", status)
        self.rabbitmq_client.publish_message(self.exchange_name, "", message)
        self.logger.info(f"Status log sent: {message}")
