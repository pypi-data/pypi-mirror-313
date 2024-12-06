import logging
from transformers import TrainerCallback
from airosentris.utils.network_utils import post_data

class MetricsCallback(TrainerCallback):
    def __init__(self, logger, project_id, run_id):
        self.project_id = project_id
        self.run_id = run_id
        self.logger = logger
        self.current_epoch = 0

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
        self.logger.log_status(self.project_id, self.run_id, "end")

    def on_evaluate(self, args, state, control, **kwargs):
        """Handles the evaluation step and logs the metrics."""
        self.logger.log_command(self.project_id, self.run_id, f"Evaluation started for step {state.global_step}.")
        
        if self.current_epoch <= args.num_train_epochs:
            metrics = state.log_history[self.current_epoch - 1]
            metrics_message = self._format_metrics(metrics)

            # Log metrics to the logger
            self.logger.log_metric(self.project_id, self.run_id, metrics_message)
            
            # Send metrics to API
            metrics_data = self._prepare_metrics_data(metrics)
            self._send_metrics_to_api(metrics_data)

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
            response = post_data(endpoint=endpoint, data=metrics_data)
            logging.info(f"Metrics sent to API: {response.json()}")
            return response
        except Exception as e:
            logging.error(f"Failed to send metrics to API: {e}")
