import json
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
    TrainerCallback,
    EarlyStoppingCallback,
)
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers.utils import logging as transformers_logging

from airosentris.algorithm.BERT.MetricsCallback import MetricsCallback
from airosentris.logger.RabbitMQLogger import RabbitMQLogger
from airosentris.message.TrainParams import TrainParams 
from airosentris.utils.network_utils import post_data

transformers_logging.set_verbosity_error()

from airosentris.trainer.BaseTrainer import BaseTrainer
from airosentris.trainer.TrainerRegistry import TrainerRegistry

import airosentris.dataset.airosentris_comment as CommentDataset

from airosentris.utils.metrics import calculate_metrics
from airosentris.utils.preprocessor import DataPreprocessor as Preprocessor


class BERTTrainer(BaseTrainer):
    def __init__(self):
        super().__init__()
        self.model = None
        self.tokenizer = None
        self.data_collator = DefaultDataCollator(return_tensors="pt")
        self.trainer = None
        self.preprocessor = Preprocessor()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.metrics = None
        self.logger = RabbitMQLogger()
        self.train_data = None
        self.test_data = None

    def init(self, train_params: TrainParams):
        self.project_id = train_params.project_id
        self.run_id = train_params.run_id
        self.logger.log_command(self.project_id, self.run_id, "Initialization started.")
        self.train_data = CommentDataset.load_data(train_params.dataset['train'])
        self.test_data = CommentDataset.load_data(train_params.dataset['test'])
        self.labels = train_params.label
        if not self.train_data or not self.test_data or not self.labels:
            logging.error("Training data, test data, or label mapping is empty.")
            raise ValueError("Training data, test data, or label mapping cannot be empty.")
        self.num_labels = len(self.labels)        
        self.train_args = TrainingArguments(
            output_dir=f"artifacts/train/{self.run_id}",
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            num_train_epochs=train_params.epoch,
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
        self.model = BertForSequenceClassification.from_pretrained(
            "indobenchmark/indobert-base-p1",
            num_labels=self.num_labels,
            cache_dir="./cache",
        ).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(
            "indobenchmark/indobert-base-p1",
            cache_dir="./cache",
        )
        self.logger.log_command(self.project_id, self.run_id, "Initialization completed.")
    
    def mapping_data(self, data):        
        try:
            df = pd.DataFrame(data)
            # df = df.sample(frac=0.005, random_state=42)
            df["label"] = df["label"].map(self.labels)
            if df["label"].isnull().any():
                logging.error("Some labels could not be mapped. Check train_labels_dict and training data.")
                raise ValueError("Label mapping failed for some labels.")
        except Exception as e:
            logging.error(f"Error processing train_data: {e}")
            raise ValueError(f"Error creating DataFrame: {e}")

        df["label"] = df["label"].astype(int)        
        
        return df
    
    def prepare_data(self, data, split_data=True):
        try:
            df = self.mapping_data(data)            
            df_preprocessed = self.preprocessor.preprocess(df)
            dataset = Dataset.from_pandas(df_preprocessed)
            tokenized_data = dataset.map(lambda x: self.tokenizer(x["text"], padding="max_length", truncation=True, max_length=128), batched=True)
            if split_data:
                return tokenized_data.train_test_split(test_size=0.2, shuffle=True, seed=42)
            return tokenized_data
        except Exception as e:
            logging.error(f"Error preparing data: {e}")
            raise ValueError(f"Error preparing data: {e}")
    
    def train(self):
        self.logger.log_command(self.project_id, self.run_id, f"Training data received with {len(self.train_data)} samples.")
        self.logger.log_command(self.project_id, self.run_id, f"Training label mapping: {self.labels}")

        tokenized_datasets = self.prepare_data(self.train_data, split_data=True)

        train_dataset = tokenized_datasets["train"]
        val_dataset = tokenized_datasets["test"]

        self.trainer = Trainer(
            model=self.model,
            args=self.train_args,
            data_collator=self.data_collator,            
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            processing_class=None,
            compute_metrics=calculate_metrics,
            callbacks=[
                MetricsCallback(self.logger, self.project_id, self.run_id),
                EarlyStoppingCallback(early_stopping_patience=3),
            ],
        )
        
        self.trainer.train()

    def evaluate(self):
        self.logger.log_command(self.project_id, self.run_id, "Evaluation started.")
        
        test_dataset = self.prepare_data(self.test_data, split_data=False)
        result = self.trainer.evaluate(test_dataset)
        logging.info(f"Test results: {result}")

        self.logger.log_command(self.project_id, self.run_id, "Evaluation completed.")

    def save_model(self):
        self.logger.log_command(self.project_id, self.run_id, "Model saving started.")        
        self.trainer.save_model(f"artifacts/models/{self.run_id}")
        self.tokenizer.save_pretrained(f"artifacts/models/{self.run_id}")
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
                post_data(api_endpoint, data)
                logging.info("Model information successfully updated.")
            except Exception as e:
                logging.error(f"An error occurred during model information update: {str(e)}")
                raise
        
        self.logger.log_command(self.project_id, self.run_id, "Model uploading completed.")

    def load_model(self, file_path):
        self.logger.log_command(self.project_id, self.run_id, f"Model loading started from {file_path}.")        
        self.logger.log_command(self.project_id, self.run_id, "Model loading completed.")

TrainerRegistry.register_trainer('BERT', BERTTrainer)