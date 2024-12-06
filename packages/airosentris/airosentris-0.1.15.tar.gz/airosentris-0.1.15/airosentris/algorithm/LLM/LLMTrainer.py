from airosentris.trainer.BaseTrainer import BaseTrainer
from airosentris.trainer.TrainerRegistry import TrainerRegistry


class LLMTrainer(BaseTrainer):
    def __init__(self):
        pass

    def train(self, data, labels):
        print(f"Training data: {data}")
        print(f"Training labels: {labels}")

    def evaluate(self, test_data, test_labels):
        print(f"Evaluating with test data: {test_data} and labels: {test_labels}")

    def save_model(self, file_path):
        print(f"Model saved to {file_path}")

    def load_model(self, file_path):
        print(f"Model loaded from {file_path}")


TrainerRegistry.register_trainer('LLM', LLMTrainer)