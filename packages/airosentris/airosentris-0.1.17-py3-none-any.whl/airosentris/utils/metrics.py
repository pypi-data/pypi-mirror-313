from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
import numpy as np
import evaluate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_metrics(eval_pred):
    try:
        accuracy_metric = evaluate.load("accuracy")
        f1_metric = evaluate.load("f1")
        recall_metric = evaluate.load("recall")
        precision_metric = evaluate.load("precision")
    except Exception as e:
        logger.error(f"Error loading metrics: {e}")
        return {}

    metrics = {}
    try:
        logits, labels = eval_pred
        predictions = np.argmax(logits, axis=-1)
        metrics["accuracy"] = accuracy_metric.compute(predictions=predictions, references=labels)
        metrics["f1"] = f1_metric.compute(predictions=predictions, references=labels, average="macro")
        metrics["recall"] = recall_metric.compute(predictions=predictions, references=labels, average="macro")
        metrics["precision"] = precision_metric.compute(predictions=predictions, references=labels, average="macro", zero_division=0)
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}")
        return {}

    logger.info(f"Metrics calculated successfully.")
    return metrics