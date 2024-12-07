import os
import shutil
import tempfile
import torch
import logging
import pandas as pd
from datasets import Dataset
from transformers import (
    BertForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
    DefaultDataCollator,
    EarlyStoppingCallback,
)
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers.utils import logging as transformers_logging

from airosentris.algorithm.BERT.MetricsCallback import MetricsCallback
from airosentris.client.APIClient import APIClient 
from airosentris.logger.TrainerLogger import TrainerLogger
from airosentris.message.TrainParams import TrainParams
from airosentris.trainer.BaseTrainer import BaseTrainer
from airosentris.trainer.TrainerRegistry import TrainerRegistry
from airosentris.dataset.airosentris_comment import load_data
from airosentris.utils.metrics import calculate_metrics
from airosentris.utils.preprocessor import DataPreprocessor
from airosentris.utils.network_utils import post_data

transformers_logging.set_verbosity_error()


class BERTTrainer(BaseTrainer):
    """
    Trainer class for fine-tuning and evaluating BERT models.
    Handles model training, evaluation, and model uploads.
    """
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger = TrainerLogger()
        self.preprocessor = DataPreprocessor()
        self.data_collator = DefaultDataCollator(return_tensors="pt")
        self.model = None
        self.tokenizer = None
        self.trainer = None
        self.train_args = None
        self.train_data = None
        self.test_data = None
        self.labels = None
        self.num_labels = None

    def init(self, train_params: TrainParams):
        """
        Initialize the BERTTrainer with dataset, labels, and training arguments.
        """
        self.project_id = train_params.project_id
        self.run_id = train_params.run_id
        self.logger.log_command(self.project_id, self.run_id, "Initialization started.")

        # Load datasets and labels
        self.train_data = load_data(train_params.dataset['train'])
        self.test_data = load_data(train_params.dataset['test'])
        self.labels = train_params.label

        self._validate_data()

        self.num_labels = len(self.labels)
        self.train_args = self._create_training_args(train_params.epoch)

        self.model = BertForSequenceClassification.from_pretrained(
            "indobenchmark/indobert-base-p1", num_labels=self.num_labels, cache_dir="./cache"
        ).to(self.device)
        self.model.config.label2id = {label: i for i, label in enumerate(self.labels)}
        self.model.config.id2label = {i: label for i, label in enumerate(self.labels)}

        self.tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p1", cache_dir="./cache")

        self.logger.log_command(self.project_id, self.run_id, "Initialization completed.")

    def _validate_data(self):
        """
        Validate the loaded training and testing data.
        """
        if not self.train_data or not self.test_data or not self.labels:
            logging.error("Training data, test data, or label mapping is empty.")
            raise ValueError("Training data, test data, or label mapping cannot be empty.")

    def _create_training_args(self, num_epochs):
        """
        Create and return TrainingArguments for the model.
        """
        return TrainingArguments(
            output_dir=f"artifacts/train/{self.run_id}",
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=num_epochs,
            weight_decay=0.01,
            save_steps=1000,
            logging_steps=100,
            logging_dir=f"artifacts/train/{self.run_id}",
            load_best_model_at_end=True,
            save_strategy="epoch",
            save_total_limit=1,
            report_to="none",
            fp16=torch.cuda.is_available(),
        )

    def prepare_data(self, data, split_data=True):
        """
        Prepare data for training and evaluation.
        """
        try:
            df = pd.DataFrame(data)
            df["label"] = df["label"].map(self.labels).astype(int)
            if df["label"].isnull().any():
                raise ValueError("Label mapping failed for some labels.")

            preprocessed_df = self.preprocessor.preprocess(df)
            dataset = Dataset.from_pandas(preprocessed_df)
            tokenized_data = dataset.map(
                lambda x: self.tokenizer(x["text"], padding="max_length", truncation=True, max_length=128), batched=True
            )
            return tokenized_data.train_test_split(test_size=0.2, shuffle=True, seed=42) if split_data else tokenized_data
        except Exception as e:
            logging.error(f"Error preparing data: {e}")
            raise ValueError(f"Error preparing data: {e}")
    
    def train(self):
        """
        Train the model using the training data.
        """
        self.logger.log_command(self.project_id, self.run_id, "Training started.")
        tokenized_datasets = self.prepare_data(self.train_data, split_data=True)

        self.trainer = Trainer(
            model=self.model,
            args=self.train_args,
            data_collator=self.data_collator,
            train_dataset=tokenized_datasets["train"],
            eval_dataset=tokenized_datasets["test"],
            compute_metrics=calculate_metrics,
            callbacks=[
                MetricsCallback(self.logger, self.project_id, self.run_id),
                EarlyStoppingCallback(early_stopping_patience=3),
            ],
        )
        self.trainer.train()
        self.logger.log_command(self.project_id, self.run_id, "Training completed.")

    def evaluate(self):
        """
        Evaluate the model on the test dataset.
        """
        self.logger.log_command(self.project_id, self.run_id, "Evaluation started.")
        test_dataset = self.prepare_data(self.test_data, split_data=False)
        result = self.trainer.evaluate(test_dataset)
        logging.info(f"Evaluation results: {result}")
        self.logger.log_command(self.project_id, self.run_id, "Evaluation completed.")

    def save_model(self):
        """
        Save the trained model and tokenizer.
        """
        model_dir = f"artifacts/models/{self.run_id}"
        self.trainer.save_model(model_dir)
        self.tokenizer.save_pretrained(model_dir)
        self.logger.log_command(self.project_id, self.run_id, "Model saving completed.")
    
    # with api
    # def upload_model(self):        
    #     self.logger.log_command(self.project_id, self.run_id, "Model uploading started.")
        
    #     with tempfile.TemporaryDirectory() as tmp_dir:            
    #         zip_file_path = os.path.join(tmp_dir, f"{self.run_id}.zip")
            
    #         model_dir = os.path.join("artifacts", "models", self.run_id)
    #         shutil.make_archive(zip_file_path.replace(".zip", ""), 'zip', model_dir)
            
    #         endpoint = "api/v1/ai-model/store"
    #         try:
    #             with open(zip_file_path, "rb") as f:
    #                 files = {"model": f.read()}                    
    #                 response = post_data(endpoint=endpoint, data={"run_id": self.run_id}, files=files, timeout=120)
                    
    #                 if response.status_code == 200:
    #                     logging.info("Model successfully sent to API")
    #                 else:
    #                     logging.error(f"Failed to send model to API. Status code: {response.status_code}, Response: {response.text}")
    #                     response.raise_for_status()
    #         except Exception as e:
    #             logging.error(f"An error occurred during model upload: {str(e)}")
    #             raise
        
    #     self.logger.log_command(self.project_id, self.run_id, "Model uploading completed.")

    # direct to minio
    def upload_model(self):
        """
        Upload the trained model to MinIO storage and update model information.
        """
        self.logger.log_command(self.project_id, self.run_id, "Model uploading started.")
        from minio import Minio
        import airosentris as air

        MINIO_BUCKET = air.Config.MINIO_BUCKET
        ACCESS_KEY = air.Config.MINIO_ACCESS_KEY
        SECRET_KEY = air.Config.MINIO_SECRET_KEY
        MINIO_API_HOST = air.Config.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
        MINIO_CLIENT = Minio(MINIO_API_HOST, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

        api_endpoint = "api/v1/run/update-model"
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_file_path = os.path.join(tmp_dir, f"{self.run_id}.zip")
            
            model_dir = os.path.join("artifacts", "models", self.run_id)
            shutil.make_archive(zip_file_path.replace(".zip", ""), 'zip', model_dir)            
            zip_file_path = zip_file_path.replace(".zip", "") + ".zip"
            
            try:
                found = MINIO_CLIENT.bucket_exists(MINIO_BUCKET)
                if not found:
                    MINIO_CLIENT.make_bucket(MINIO_BUCKET)
                else:
                    logging.info(f"Bucket {MINIO_BUCKET} already exists.")
                
                MINIO_CLIENT.fput_object(MINIO_BUCKET, f"model/{self.run_id}.zip", zip_file_path)
                logging.info("Model successfully uploaded to MinIO.")
            except Exception as e:
                logging.error(f"An error occurred during model upload to MinIO: {str(e)}")
                raise

            try:
                data = {
                    "run_id": self.run_id,
                    "model_file_name": f"{self.run_id}.zip",
                    "model_url": f"{MINIO_API_HOST}/{MINIO_BUCKET}/model/{self.run_id}.zip"
                }
                self.api_client.post_data(api_endpoint, data)
                logging.info("Model information successfully updated.")
            except Exception as e:
                logging.error(f"An error occurred during model information update: {str(e)}")
                raise
        
        self.logger.log_command(self.project_id, self.run_id, "Model uploading completed.")
        self.logger.log_status(self.project_id, self.run_id, "end")

    def load_model(self, file_path):
        self.logger.log_command(self.project_id, self.run_id, f"Model loading started from {file_path}.")        
        self.logger.log_command(self.project_id, self.run_id, "Model loading completed.")

TrainerRegistry.register_trainer('BERT', BERTTrainer)