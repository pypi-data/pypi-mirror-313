import logging
import json
import time
from threading import Thread

import pika
from airosentris.agent.Agent import Agent
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent
from airosentris.client.RabbitMQClient import RabbitMQClient
from airosentris.hardware.SystemInfo import SystemInfo
from airosentris.message.AgentStatus import AgentStatusRequest
from airosentris.message.TrainParams import TrainParams
from airosentris.trainer.TrainerFactory import TrainerFactory


class TrainerService:
    def __init__(self):
        self.agent = get_agent()
        self.agent_id = str(self.agent['id'])

        self.training_exchange = 'airosentris.train'
        self.training_queue = f'airosentris.train.queue.{self.agent_id}'
        self.agent_status_queue = f'airosentris.agent-{self.agent_id}'

        self.on_agent_status_request = self.process_agent_status_request
        self.on_training_request = self.process_training_request
        
        self.config = get_config()

        self.training_rabbitmq_client = None
        self.agent_rabbitmq_client = None
        self.training_listener_thread = None
        self.agent_listener_thread = None

    def initialize_trainer_queue(self):
        self.training_rabbitmq_client = RabbitMQClient(self.config, heartbeat=3600, blocked_connection_timeout=600)
        self.training_rabbitmq_client.connect()
        self.training_rabbitmq_client.declare_exchange(self.training_exchange, exchange_type='direct')
        self.training_rabbitmq_client.declare_queue(self.training_queue)
        self.training_rabbitmq_client.bind_queue(self.training_exchange, self.training_queue, self.agent_id)

    def handle_agent_queries(self):
        if not callable(self.on_agent_status_request):
            raise ValueError("on_agent_status_request callback must be callable")
        while True:
            try:
                self.agent_rabbitmq_client = RabbitMQClient(self.config)
                self.agent_rabbitmq_client.connect()
                self.agent_rabbitmq_client.declare_exchange('airosentris.agent', exchange_type='fanout')
                self.agent_rabbitmq_client.declare_queue(self.agent_status_queue, durable=False, auto_delete=True)
                self.agent_rabbitmq_client.bind_queue('airosentris.agent', self.agent_status_queue, '')

                def on_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        message_receive = AgentStatusRequest(code=message.get("code"))
                        self.on_agent_status_request(message_receive)
                    except Exception as e:
                        logging.error(f"Error processing agent info message: {e}")
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                
                self.agent_rabbitmq_client.consume_messages(self.agent_status_queue, on_message)
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.StreamLostError as e:
                logging.error(f"Stream connection lost: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in provide_query: {e}")
                break

    def watch_training_requests(self):
        if not callable(self.on_training_request):
            raise ValueError("on_training_request callback must be callable")
        while True:
            try:
                self.initialize_trainer_queue()

                def on_message(ch, method, properties, body):
                    try:
                        message_dict = json.loads(body)
                        train_params = TrainParams(
                            project_id=message_dict.get("project_id"),
                            run_id=message_dict.get("run_id"),
                            algorithm=message_dict.get("algorithm"),
                            scope=message_dict.get("scope"),
                            label=message_dict.get("label"),
                            dataset=message_dict.get("dataset"),
                            params=message_dict.get("params"),
                            epoch=message_dict.get("epoch")
                        )

                        # Handle tuples in train_params
                        for key, value in train_params.__dict__.items():
                            if isinstance(value, tuple):
                                setattr(train_params, key, value[0])

                        self.on_training_request(train_params)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except json.JSONDecodeError as e:
                        logging.error(f"Invalid JSON message: {e}")
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as e:
                        logging.error(f"Error processing training message: {e}")
                        ch.basic_ack(delivery_tag=method.delivery_tag)

                self.training_rabbitmq_client.channel.basic_qos(prefetch_count=1)
                self.training_rabbitmq_client.consume_messages(self.training_queue, on_message)
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.StreamLostError as e:
                logging.error(f"Stream connection lost: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in watch_training_requests: {e}")
                break

    def process_training_request(self, train_params: TrainParams):
        logging.info(f"Processing training request: {train_params}")
        try:
            trainer_class = TrainerFactory.get_trainer(train_params.algorithm)
            trainer_algorithm = trainer_class()
            trainer_algorithm.init(train_params)
            trainer_algorithm.train()
            trainer_algorithm.evaluate()
            trainer_algorithm.save_model()
            trainer_algorithm.upload_model()
        except Exception as e:
            logging.error(f"Error processing training request: {e}")


    def process_agent_status_request(self, message_receive: AgentStatusRequest):
        logging.info(f"Processing agent status request: {message_receive}")
        try:
            system_info = SystemInfo.get_common_info()

            agent = Agent()
            result = agent.update(system_info)
            logging.info(f"Processed agent Request message: {result}")
        except Exception as e:
            logging.error(f"Error processing agent status request: {e}")

    def start_agent_query_listener(self):
        self.agent_listener_thread = Thread(target=self.handle_agent_queries)
        self.agent_listener_thread.start()

    def start_training_request_listener(self):
        self.training_listener_thread = Thread(target=self.watch_training_requests)
        self.training_listener_thread.start()
        self.training_listener_thread.join()

    def start(self):
        if not callable(self.on_training_request):
            raise ValueError("on_training_request callback must be set before starting the trainer")
        self.start_agent_query_listener()
        self.start_training_request_listener()
