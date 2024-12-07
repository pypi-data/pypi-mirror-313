import logging
from transformers import TrainerCallback
from airosentris.client.APIClient import APIClient
from airosentris.logger.TrainerLogger import TrainerLogger


class MetricsCallback(TrainerCallback):
    def __init__(self, logger : TrainerLogger, project_id, run_id):
        self.api_client = APIClient()
        self.project_id = project_id
        self.run_id = run_id
        self.logger = logger
        self.current_epoch = 0
        self.end_of_train = False

    def on_epoch_begin(self, args, state, control, **kwargs):
        """Increments the current epoch at the beginning of each epoch."""
        self.current_epoch += 1
        self.logger.log_command(self.project_id, self.run_id, f"Epoch {self.current_epoch} started.")

    def on_epoch_end(self, args, state, control, **kwargs):
        """Logs the end of the current epoch."""
        self.logger.log_command(self.project_id, self.run_id, f"Epoch {self.current_epoch} ended.")

    def on_train_end(self, args, state, control, **kwargs):
        """Logs the end of training."""
        self.logger.log_command(self.project_id, self.run_id, "Training ended.")   
        self.end_of_train = True

    def on_log(self, args, state, control, logs=None, **kwargs):
        """Logs the metrics for the current epoch."""
        if self.end_of_train:
            return

        for log in state.log_history:
            if log["epoch"] == float(self.current_epoch) and "eval_loss" in log:
                metrics_message = self._format_metrics(log)

                self.logger.log_metric(self.project_id, self.run_id, metrics_message)
                
                metrics_data = self._prepare_metrics_data(log)
                self._send_metrics_to_api(metrics_data)
                break
            
    def on_evaluate(self, args, state, control, **kwargs):
        """Handles the evaluation step and logs the metrics."""
        self.logger.log_command(self.project_id, self.run_id, f"Evaluation started for epoch {state.epoch} and step {state.global_step}.")
        

    def _format_metrics(self, metrics):
        """Formats the metrics into a structured dictionary."""
        return {
            "epoch": int(metrics["epoch"]),
            "accuracy": round(metrics["eval_accuracy"]["accuracy"], 2),
            "f1_score": round(metrics["eval_f1"]["f1"], 2),
            "precision": round(metrics["eval_precision"]["precision"], 2),
            "recall": round(metrics["eval_recall"]["recall"], 2),
            "loss": round(metrics["eval_loss"], 2),
            "runtime": round(metrics["eval_runtime"], 2),
            "samples_per_second": round(metrics["eval_samples_per_second"], 2),
            "steps_per_second": round(metrics["eval_steps_per_second"], 2),
            "step": int(metrics["step"])
        }

    def _prepare_metrics_data(self, metrics):
        """Prepares the metrics data for API transmission."""
        return {
            "run_id": self.run_id,
            "epoch": int(metrics["epoch"]),
            "accuracy": round(metrics["eval_accuracy"]["accuracy"], 2),
            "f1_score": round(metrics["eval_f1"]["f1"], 2),
            "precision": round(metrics["eval_precision"]["precision"], 2),
            "recall": round(metrics["eval_recall"]["recall"], 2),
        }

    @staticmethod
    def _send_metrics_to_api(metrics_data):
        """Sends the metrics data to an external API."""
        endpoint = "api/v1/run/log"
        try:
            logging.info(f"Sending metrics to API: {metrics_data}")
            api_client = APIClient()
            response = api_client.post_data(endpoint=endpoint, data=metrics_data)
            logging.info(f"Metrics sent to API: {response.json()}")
            return response
        except Exception as e:
            logging.error(f"Failed to send metrics to API: {e}")
