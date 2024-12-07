import logging
from airosentris.runner.BaseRunner import BaseRunner
from airosentris.runner.RunnerRegistry import RunnerRegistry


class LLMRunner(BaseRunner):
    def __init__(self):
        super().__init__()        
        self.model = None
        self.scope_code = None

    def load_model(self, scope_code, model_path):
        """Load the model into the appropriate pipeline."""
        try:            
            logging.info(f"Model for {scope_code} loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model for {scope_code}: {e}")

    def evaluate(self, comment):        
        comment_id = comment.id
        comment_text = comment.content
        return None

RunnerRegistry.register_runner('LLM', LLMRunner)