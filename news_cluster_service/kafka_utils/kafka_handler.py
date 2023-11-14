import os
import json
import socket
from kafka import KafkaConsumer
from concurrent.futures import ThreadPoolExecutor


class KafkaHandler:

	def __init__(self):

		self.time_out = 5
		self.batch_size = 500
		self.message_future = None
		self.vital_keys = ["hash", "common_key"]

		self.config = self.get_kafka_config()
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.consumer = self.initiate_consumer(config=self.config)

	def get_kafka_config(self):

		kafka_config = {
			"host": os.environ.get("KAFKA_HOST"),
			"port": os.environ.get("KAFKA_PORT"),
			"topic": os.environ.get("KAFKA_TOPIC"),
			"group": os.environ.get("KAFKA_GROUP")
		}

		return kafka_config

	def initiate_consumer(self, config: dict):

		consumer = KafkaConsumer(
			config["topic"],
			bootstrap_servers=[f"{config['host']}:{config['port']}"],
			group_id=config["group"],
			value_deserializer=lambda x: json.loads(x.decode('utf-8'))
		)

		return consumer

	def consume_message(self):

		message = next(self.consumer)

		return message.value

	def get_batch_data(self):

		fatal_error = ""
		batch_data, batch_ids  = [], []
		batch_size = self.batch_size

		while batch_size > 0:
			
			if not self.kafka_available():
				fatal_error = "Kafka server is down"
				break

			if self.message_future is None:
				self.message_future = \
					self.executor.submit(self.consume_message)

			try:
				data = self.message_future.result(timeout=self.time_out)
				self.message_future = None

				if (not isinstance(data, dict) or
					not all(k in data.keys() for k in self.vital_keys)):
					
					continue

				data.pop("hash", None)
				batch_data.append(data)
				batch_ids.append(data["common_key"])
				batch_size -= 1

			except Exception as e:
				fatal_error = str(e)
				break

		return batch_data, batch_ids, fatal_error

	def kafka_available(self):
		
		try:
			socket.create_connection(
				(self.config["host"], self.config["port"]))

			return True

		except (socket.timeout, ConnectionRefusedError):

			return False
