from traceback import format_exc
from logger.app_logger import AppLogger
from pymongo.errors import BulkWriteError


class QueryUtils:

	"""
	A class containing a set of functionalities to 
	interact with Mongo database

	...

	Attributes:
		None
	"""

	def __init__(self):

		self.db_logger = AppLogger()
		self.db_logger.create_log("mongodb_query_error")

	def filter_docs(self, collection, doc_ids: list):
		"""
		Filter out document ids which already exist
		in database.

		Args:
			collection: A MongoClient collection object 
			doc_ids: Set of document ids

		Returns:
			List of non-existent document ids
		"""

		try:
			response = collection.find(
				{"common_key": { "$in": doc_ids }}, 
				{"common_key": True, "_id": False})

			existing_ids = [ data["common_key"] for data in response ]
			non_existent_ids = list(set(doc_ids).difference(existing_ids))

		except:
			self.db_logger.submit_info_log(
				message=format_exc())
			non_existent_ids = []

		return non_existent_ids

	def insert_docs(self, collection, docs: list):
		"""
		Insert a list of input documents using Bulk insertion
		approach and capture any unexpected error.

		Args:
			collection: A MongoClient collection object 
			docs: Set of documents to insert

		Returns:
			None
		"""

		try:
			if docs:
				collection.insert_many(docs, ordered=False)

			else:
				self.db_logger.submit_info_log(
					message="No data to insert!")

		except BulkWriteError: pass

		except:
			self.db_logger.submit_info_log(
				message=format_exc())
