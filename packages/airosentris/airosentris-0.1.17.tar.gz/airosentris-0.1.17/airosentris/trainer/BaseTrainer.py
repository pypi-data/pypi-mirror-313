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