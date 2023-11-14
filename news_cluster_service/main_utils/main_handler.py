import sys
import pandas as pd
from time import sleep
from logger.app_logger import AppLogger
from kafka_utils.kafka_handler import KafkaHandler
from cluster_utils.ClusterService import newsCluster
from mongodb.initializer import query_utils, mongo_cache_collection


class MainHandler:

	def __init__(self):

		self.retry_interval = 2

		self.main_logger = AppLogger()
		self.main_logger.create_log("main")

		self.news_cluster = newsCluster()
		self.kafka_handler = KafkaHandler()

	def run(self):

		while True:

			dataset, dataset_ids, error = \
				self.kafka_handler.get_batch_data()

			if error:
				self.main_logger.submit_info_log(
					message=error)
				sys.exit()			

			if not dataset:
				self.main_logger.submit_info_log(
					message="No news from rss producer")
				sleep(self.retry_interval * 60)
				continue

			filtered_dataset = self.filter_data(
				dataset=dataset, dataset_ids=dataset_ids)

			if not filtered_dataset:
				self.main_logger.submit_info_log(
					message="Duplicate news from rss producer")
				continue

			df = pd.DataFrame(filtered_dataset)

			clustered_df = \
				self.news_cluster.getDocumentsClass(
					data_frame=df)

			clustered_dataset = self.structure_data(
				df=clustered_df)

			self.main_logger.submit_info_log(
				message=(
					f"received news = {len(dataset)}\n"
					f"filtered news = {len(filtered_dataset)}\n"
					f"important news = {len(clustered_dataset)}\n"
					f"last received news - id = {dataset[-1]['common_key']} , time = {dataset[-1]['time']}"))

			query_utils.insert_docs(
				collection=mongo_cache_collection,
				docs=clustered_dataset)

	def filter_data(self, dataset, dataset_ids):

		non_existent_ids = query_utils.filter_docs(
			collection=mongo_cache_collection,
			doc_ids=dataset_ids)

		filtered_dataset = [ data for data in dataset if data["common_key"] in non_existent_ids ]

		return filtered_dataset

	def structure_data(self, df):

		dataset = []

		for _, data in df.iterrows():

			data = data.to_dict()
			if data["important"]:

				data["is_tagged"] = False
				dataset.append(data)

		return dataset
