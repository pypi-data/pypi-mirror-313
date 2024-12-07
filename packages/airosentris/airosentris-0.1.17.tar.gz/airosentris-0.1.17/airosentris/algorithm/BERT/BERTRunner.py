import logging
import os
import threading
import time
from transformers import pipeline

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from airosentris.runner.BaseRunner import BaseRunner
from airosentris.runner.RunnerRegistry import RunnerRegistry
from airosentris.utils.network_utils import post_data, fetch_data
from airosentris.client.APIClient import APIClient

load_dotenv()

class ComplaintCategory(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    complaint_category: str = Field(..., title="Complaint Category", description="The category of the complaint")

class StatementType(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    statement_type: str = Field(..., title="Statement Type", description="The type of the statement")

class Sentiment(BaseModel):
    comment: str = Field(..., title="Comment Text", description="The text of the comment to be evaluated")
    sentiment: str = Field(..., title="Sentiment", description="The sentiment of the comment")

class BERTRunner(BaseRunner):
    def __init__(self):
        super().__init__()
        self.model_chat = ChatGroq(
            # groq_api_key=os.getenv('GROQ_API_KEY'),
            groq_api_key='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',
            model_name='llama3-70b-8192'
        )
        self.model = None
        self.scope_code = None

    def load_model(self, scope_code, model_path):
        """Load the model into the appropriate pipeline."""
        try:
            self.scope_code = scope_code
            if scope_code == "sentiment":
                self.model = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path, device=None)                
            else:
                self.model = pipeline("text-classification", model=model_path, tokenizer=model_path, device=None)
            
            logging.info(f"Model for {scope_code} loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading model for {scope_code}: {e}")

    def evaluate(self, comment):        
        comment_id = comment.id
        comment_text = comment.content

        if self.model:
            result = self.model(comment_text)
            logging.info(f"Result:{result}")
            result = result[0]['label'].lower()
            self.send_tag_to_api(comment_id, self.scope_code, result)
            return result
        return None

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
            

RunnerRegistry.register_runner('BERT', BERTRunner)