import logging
import os
import threading
import time
from transformers import pipeline

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from airosentris.utils.network_utils import post_data, fetch_data

load_dotenv()

class ComplaintCategory(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    category: str = Field(..., title="Complaint Category", description="The category of the complaint")

class StatementType(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    statement_type: str = Field(..., title="Statement Type", description="The type of the statement")

class Sentiment(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    sentiment: str = Field(..., title="Sentiment", description="The sentiment of the comment")

class BERTRunner:
    def __init__(self):
        # self.sentiment_model_dir = "models/sentiment_analisis_indonlu"
        # self.sentiment_pipeline = pipeline("sentiment-analysis",
        #                                    model=self.sentiment_model_dir,
        #                                    tokenizer=self.sentiment_model_dir, 
        #                                    device=None)
        # self.complaint_pipeline = None
        # self.statement_pipeline = None
        self.model_chat = ChatGroq(
            # groq_api_key=os.getenv('GROQ_API_KEY'),
            groq_api_key='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',
            model_name='llama3-70b-8192'
        )
        self.scopes = [
            "complaint_category",
            "sentiment",
            "statement_type"
        ]
        self.models = {}
        self.model_cache = {}
    
    def get_active_model(self, scope_code):
        """Fetch the active model details for a specific scope."""
        endpoint = "api/v1/ai-model/active/detail"        
        data = {"scope_code": scope_code}
        
        try:
            response = post_data(endpoint=endpoint, data=data)
            if response.status_code == 200:
                model_details = response.json()
                return model_details.get('data', None)
            else:
                logging.error(f"Error retrieving active model for {scope_code}: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Error fetching active model for {scope_code}: {e}")
            return None

    # with api
    # def download_model(self, run_id, scope_code):
    #     """Download the model using the provided run_id."""
    #     endpoint = f"api/v1/ai-model/download/{run_id}/agent"
        
    #     try:
    #         response = fetch_data(endpoint=endpoint, stream=True)
    #         if response.status_code == 200:
    #             model_path = f"tmp/{scope_code}.zip"                
    #             with open(model_path, 'wb') as f:
    #                 for chunk in response.iter_content(chunk_size=8192):
    #                     if chunk:
    #                         f.write(chunk)
                
    #             os.system(f"unzip {model_path} -d models/")      
    #             # os.remove(model_path)                
    #             logging.info(f"Model for {scope_code} downloaded and saved at {model_path}")
    #             return model_path
    #         else:
    #             logging.error(f"Error downloading model for {scope_code}: {response.text}")
    #             return None
    #     except Exception as e:
    #         logging.error(f"Error downloading model for {scope_code}: {e}")
    #         return None

    # direct to minio
    def download_model(self, run_id):
        """Download the model using the provided run_id."""
        import tempfile
        from minio import Minio
        import airosentris as air

        MINIO_BUCKET = air.Config.MINIO_BUCKET
        ACCESS_KEY = air.Config.MINIO_ACCESS_KEY
        SECRET_KEY = air.Config.MINIO_SECRET_KEY
        MINIO_API_HOST = air.Config.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
        MINIO_CLIENT = Minio(MINIO_API_HOST, access_key=ACCESS_KEY, secret_key=SECRET_KEY, secure=False)

        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                model_path = os.path.join(tmp_dir, f"{run_id}.zip")
                MINIO_CLIENT.fget_object(MINIO_BUCKET, f"model/{run_id}.zip", model_path)
                os.system(f"unzip {model_path} -d artifacts/models/")      
                logging.info(f"Model for {run_id} downloaded and saved at {model_path}")
                return f"artifacts/models/{run_id}"
        except Exception as e:
            logging.error(f"Error downloading model for {run_id}: {e}")
            return None

    def load_model(self, scope_code, model_path):
        """Load the model into the appropriate pipeline."""
        try:
            if scope_code == "sentiment":
                model = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path, device=None)
            else:
                model = pipeline("text-classification", model=model_path, tokenizer=model_path, device=None)

            self.models[scope_code] = model
            logging.info(f"Model for {scope_code} loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model for {scope_code}: {e}")

    def update_model_for_scope(self, scope_code):
        """Fetch, download, and load the model for the given scope."""
        # Fetch the active model details
        active_model = self.get_active_model(scope_code)
        if not active_model:
            logging.warning(f"No active model found for {scope_code}.")
            return
        logging.info(f"Active model for {scope_code}: {active_model}")
        run_id = active_model.get('run_id', None)
        if run_id:
            # Check if model is already cached
            if scope_code not in self.model_cache or self.model_cache[scope_code] != run_id:
                model_path = self.download_model(run_id)
                if model_path:
                    self.load_model(scope_code, model_path)
                    self.model_cache[scope_code] = run_id
            else:
                logging.info(f"Model for {scope_code} is already up-to-date.")
        else:
            logging.error(f"Model ID not found for {scope_code}.")

    def auto_update_thread(self):
        """Thread function to auto-update the models."""
        while True:
            for scope_code in self.scopes:
                self.update_model_for_scope(scope_code)
            logging.info("Models updated successfully.")            
            time.sleep(300)

    def auto_update(self):
        """Method to start the auto-update thread."""
        update_thread = threading.Thread(target=self.auto_update_thread)
        update_thread.start()

    def evaluate_sentiment(self, comment_text, result):
        """ Thread function for evaluating sentiment """
        try:
            sentiment_model = self.models.get('sentiment', None)
            if not sentiment_model:
                return self.zs_sentiment(comment_text, result)
            sentiment_result = sentiment_model(comment_text)
            result['sentiment'] = sentiment_result[0]['label'].lower()
            logging.info(f"Sentiment result: {sentiment_result}")
        except Exception as e:
            result['sentiment'] = None
            logging.error(f"Error evaluating sentiment: {e}")

    def evaluate_statement(self, comment_text, result):
        """ Thread function for evaluating statement type """
        try:
            statement_model = self.models.get('statement_type', None)
            if not statement_model:
                return self.zs_statement(comment_text, result)
            statement_result = statement_model(comment_text)
            result['statement_type'] = statement_result[0]['label'].lower()
            logging.info(f"Statement type result: {statement_result}")
        except Exception as e:
            result['statement_type'] = None
            logging.error(f"Error evaluating statement type: {e}")
    
    def evaluate_complaint(self, comment_text, result):
        """ Thread function for evaluating complaint category """
        try:
            complaint_model = self.models.get('complaint_category', None)
            if not complaint_model:
                return self.zs_complaint(comment_text, result)
            complaint_result = complaint_model(comment_text)
            result['complaint_category'] = complaint_result[0]['label'].lower()
            logging.info(f"Complaint category result: {complaint_result}")
        except Exception as e:
            result['complaint_category'] = None
            logging.error(f"Error evaluating complaint category: {e}")

    def zs_sentiment(self, comment_text, result):
        """Thread function for evaluating sentiment."""
        try:
            parser = JsonOutputParser(pydantic_object=Sentiment)
            valid_sentiments = ["positive", "negative", "neutral"]

            prompt = PromptTemplate(
                template=(
                    "Classify the following comment into exactly one of these sentiments: positive, negative, neutral. "
                    "Provide your answer as a single word from the list above. "
                    "You must always return valid JSON fenced by a markdown code block. Do not return any additional text."
                    "Do not include any additional text or explanation.\n\n"
                    "Comment: {comment}\n{format_instructions}"
                ),
                input_variables=["comment"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

            chain = prompt | self.model_chat | parser
            sentiment_result = chain.invoke({"comment": comment_text})

            sentiment = sentiment_result.get('sentiment')
            if sentiment in valid_sentiments:
                result['sentiment'] = sentiment
            else:
                result['sentiment'] = None

            logging.info(f"Sentiment result: {sentiment_result}")
        except Exception as e:
            result['sentiment'] = None
            logging.error(f"Error evaluating sentiment: {e}")

    def zs_statement(self, comment_text, result):
        """Thread function for evaluating statement type."""
        try:
            parser = JsonOutputParser(pydantic_object=StatementType)
            valid_statement_types = ["question", "statement"]

            prompt = PromptTemplate(
                template=(
                    "Classify the following comment into exactly one of these types: question, statement. "
                    "Provide your answer as a single word from the list: question, statement. "
                    "You must always return valid JSON fenced by a markdown code block. Do not return any additional text."
                    "Do not include any additional text or explanation.\n\n"
                    "Comment: {comment}\n{format_instructions}"
                ),
                input_variables=["comment"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )

            chain = prompt | self.model_chat | parser
            statement_result = chain.invoke({"comment": comment_text})

            statement_type = statement_result.get('statement_type')
            if statement_type in valid_statement_types:
                result['statement_type'] = statement_type
            else:
                result['statement_type'] = None

            logging.info(f"Statement type result: {statement_result}")
        except Exception as e:
            result['statement_type'] = None
            logging.error(f"Error evaluating statement type: {e}")

    def zs_complaint(self, comment_text, result):
        """Thread function for evaluating complaint category."""
        try:
            parser = JsonOutputParser(pydantic_object=ComplaintCategory)
            valid_categories = [
                "air_keruh", "aliran_air", "apresiasi", "kebocoran",
                "layanan", "meter", "pemakaian_tagihan", "tarif", "tda"
            ]
            
            prompt = PromptTemplate(
                template=(
                    "Classify the following comment into exactly one of these categories: "
                    "air_keruh, aliran_air, apresiasi, kebocoran, layanan, meter, pemakaian_tagihan, tarif, tda. "
                    "Provide your answer as a single word from the list above. "
                    "You must always return valid JSON fenced by a markdown code block. Do not return any additional text."
                    "Do not include any additional text or explanation.\n\n"
                    "Comment: {comment}\n{format_instructions}"
                ),
                input_variables=["comment"],
                partial_variables={"format_instructions": parser.get_format_instructions()},
            )
            
            chain = prompt | self.model_chat | parser
            complaint_category_result = chain.invoke({"comment": comment_text})
            
            category = complaint_category_result.get('category')
            if category in valid_categories:
                result['complaint_category'] = category
            else:
                result['complaint_category'] = None
            
            logging.info(f"Complaint category result: {complaint_category_result}")
        except Exception as e:
            result['complaint_category'] = None
            logging.error(f"Error evaluating complaint category: {e}")

    def evaluate(self, comment_id, comment_text):
        """ Method to evaluate the text using 3 threads """        
        result = {}
        
        try:
            sentiment_thread = threading.Thread(target=self.evaluate_sentiment, args=(comment_text, result))
            statement_type_thread = threading.Thread(target=self.evaluate_statement, args=(comment_text, result))
            complaint_category_thread = threading.Thread(target=self.evaluate_complaint, args=(comment_text, result))
            
            sentiment_thread.start()
            statement_type_thread.start()
            complaint_category_thread.start()
            
            sentiment_thread.join()
            statement_type_thread.join()
            complaint_category_thread.join()
            
            logging.info(f"Evaluation result: {result}")

            if 'complaint_category' in result and result['complaint_category']:
                self.send_tag_to_api(comment_id, 'complaint_category', result['complaint_category'])
            if 'sentiment' in result and result['sentiment']:
                self.send_tag_to_api(comment_id, 'sentiment', result['sentiment'])
            if 'statement_type' in result and result['statement_type']:
                self.send_tag_to_api(comment_id, 'statement_type', result['statement_type'])
            
        except Exception as e:
            logging.error(f"Error during evaluation: {e}")
            result = {
                'sentiment': None,
                'statement_type': None,
                'complaint_category': None
            }
        
        return result

    def send_tag_to_api(self, comment_id, scope_code, scope_label_code):
        """ Method to send the tag to the API """

        endpoint = "api/v1/comment/tag/agent"        

        payload = {
            "comment_id": comment_id,
            "scopes_code": scope_code,
            "scopes_label_code": scope_label_code
        }

        try:
            response = post_data(endpoint=endpoint, data=payload)
            if response.status_code == 200:
                logging.info(f"Successfully tagged comment {comment_id} with {scope_code}: {scope_label_code}")
            else:
                logging.error(f"Failed to tag comment {comment_id} with {scope_code}: {scope_label_code}, Response: {response.text}")
        except Exception as e:
            logging.error(f"Error sending tag to API: {e}")