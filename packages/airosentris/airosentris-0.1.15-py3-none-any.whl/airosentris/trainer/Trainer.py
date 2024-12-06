import pika
import json
import time
import logging
from threading import Thread
from airosentris.agent.Agent import Agent
from airosentris.config.ConfigFetcher import get_config
from airosentris import get_agent
from airosentris.hardware.SystemInfo import SystemInfo
from airosentris.logger.RabbitMQLogger import RabbitMQLogger
from airosentris.message.AgentStatus import AgentStatusRequest
from airosentris.message.TrainParams import TrainParams
from airosentris.trainer.TrainerFactory import TrainerFactory


class Trainer:

    def __init__(self):
        self.agent = get_agent()
        self.agent_id = str(self.agent['id'])

        self.trainer_exchange_name = 'airosentris.train'
        self.trainer_queue_name = 'airosentris.train.queue.{}'.format(self.agent_id)

        self.agent_query_queue = 'airosentris.agent-{}'.format(self.agent_id)
        self.on_request_agent_info = self.agent_callback
        self.on_new_message = self.train_callback
        
        self.train_thread = None
        self.agent_thread = None

    def _connect(self, config: dict) -> tuple:
        try:
            credentials = pika.PlainCredentials(config['username'], config['password'])
            parameters = pika.ConnectionParameters(
                host=config['host'],
                port=int(config['port']),
                virtual_host=config['vhost'],
                credentials=credentials,
                heartbeat=3600,
                blocked_connection_timeout=600 
            )
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            return connection, channel
        except pika.exceptions.AMQPConnectionError as e:
            logging.error(f"AMQP Connection error: {e}")
            raise
        except pika.exceptions.ProbableAuthenticationError as e:
            logging.error(f"Authentication error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error during connection: {e}")
            raise

    def _setup_queue_and_exchange(self, channel):
        try:
            # Declare the exchange (type: direct or topic)
            channel.exchange_declare(exchange=self.trainer_exchange_name, exchange_type='direct', durable=True)
            logging.info(f"Exchange '{self.trainer_exchange_name}' declared successfully.")

            # Declare the queue
            channel.queue_declare(queue=self.trainer_queue_name, durable=True)
            logging.info(f"Queue '{self.trainer_queue_name}' declared successfully.")

            routing_key = self.agent_id
            channel.queue_bind(exchange=self.trainer_exchange_name,
                               queue=self.trainer_queue_name,
                               routing_key=routing_key)

            logging.info(f"Queue '{self.trainer_queue_name}' "
                         f"bound to exchange '{self.trainer_exchange_name}' "
                         f"with routing key '{routing_key}'.")

        except Exception as e:
            logging.error(f"Failed to setup queue and exchange: {e}")
            raise
    
    def provide_query(self) -> None:
        if self.on_request_agent_info is None:
            raise ValueError("on_request_agent_info callback must be provided and must be callable")

        while True:
            try:
                config = get_config()
                connection, channel = self._connect(config)

                channel.exchange_declare(exchange='airosentris.agent', exchange_type='fanout', durable=True)

                queue_result = channel.queue_declare(queue=self.agent_query_queue, auto_delete=True, durable=False)
                queue_name = queue_result.method.queue

                channel.queue_bind(exchange='airosentris.agent', queue=queue_name)

                def on_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        message_receive = AgentStatusRequest(
                            code=message.get("code")
                        )
                        self.on_request_agent_info(message_receive)
                    except Exception as e:
                        logging.error(f"Error processing message: {e}")

                channel.basic_consume(queue=self.agent_query_queue, on_message_callback=on_message, auto_ack=True)
                logging.info(f"[*] Waiting for messages in {self.agent_query_queue}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.StreamLostError as e:
                logging.error(f"Stream connection lost: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Error in provide_query method: {e}")
                break

    def watch(self):
        if self.on_new_message is None:
            raise ValueError("on_new_message callback must be provided and must be callable")

        while True:
            try:
                config = get_config()
                logging.info(f"RabbitMQ Configuration: {config}")
                connection, channel = self._connect(config)

                self._setup_queue_and_exchange(channel)

                def on_message(ch, method, properties, body):
                    try:
                        # Attempt to parse the message
                        message_dict = json.loads(body)

                        # Convert to dict
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

                        # Handling train params if got tuple
                        for key, value in train_params.__dict__.items():
                            if isinstance(value, tuple):
                                setattr(train_params, key, value[0])                                

                        self.on_new_message(train_params)

                        # Acknowledge the message after successful processing
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except json.JSONDecodeError as e:
                        # Handle invalid JSON
                        logging.error(f"Invalid JSON: {e}. Body: {body}")
                        # Acknowledge the message to prevent re-delivery
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as e:
                        # Handle any other errors
                        logging.error(f"Error processing message: {e}")
                        # Acknowledge the message to prevent re-delivery
                        ch.basic_ack(delivery_tag=method.delivery_tag)

                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=self.trainer_queue_name, on_message_callback=on_message)
                logging.info(f"[*] Waiting for messages in {self.trainer_queue_name}. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Connection error: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except pika.exceptions.StreamLostError as e:
                logging.error(f"Stream connection lost: {e}. Reconnecting in 5 seconds...")
                time.sleep(5)
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                break

    def train_callback(self, train_params: TrainParams):
        try:
            
            rabbitmq_config = get_config()
            rabbitmq_logger = RabbitMQLogger(rabbitmq_config)

            rabbitmq_logger.log_status( train_params.project_id,  train_params.run_id, "start" )

            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Processing message: {train_params.run_id}" )        
            
            trainer_class = TrainerFactory.get_trainer(train_params.algorithm)
            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Load Train Algorithm: {train_params.algorithm}")
            trainer_algorithm = trainer_class()
            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Init Train Algorithm...")
            trainer_algorithm.init(train_params)
            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Train model...")
            trainer_algorithm.train()

            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Evaluate model...")
            trainer_algorithm.evaluate()        

            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Save model...")
            trainer_algorithm.save_model()
            
            rabbitmq_logger.log_command( train_params.project_id,  train_params.run_id, f"Upload model...")
            trainer_algorithm.upload_model()

        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def agent_callback(self, message_receive: AgentStatusRequest) -> None:
        logging.info(f"Handle incoming agent message: {message_receive}")
        system_info = SystemInfo.get_common_info()

        agent = Agent()
        result = agent.update(system_info)
        logging.info(f"Processed agent Request message: {result}")

    def start_agent_thread(self):
        self.agent_thread = Thread(target=self.provide_query)
        self.agent_thread.start()

    def start_train_thread(self):
        self.train_thread = Thread(target=self.watch)
        self.train_thread.start()
        self.train_thread.join()

    def start(self):
        if self.on_new_message is None:
            raise ValueError("on_new_message callback must be set before starting the trainer")
        self.start_agent_thread()
        self.start_train_thread()        
