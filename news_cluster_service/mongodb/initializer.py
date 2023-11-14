import os
from mongodb.query_utils import QueryUtils
from mongodb.connection_utils import MongoConfig, MongoConnect


query_utils = QueryUtils()
mongo_connect = MongoConnect()

mongo_cache_config = MongoConfig(
	user=os.environ.get("MONGO_CACHE_USERNAME"),
	password=os.environ.get("MONGO_CACHE_PASSWORD"),
	host=os.environ.get("MONGO_CACHE_HOST"),
	port=os.environ.get("MONGO_CACHE_PORT"),
	name=os.environ.get("MONGO_CACHE_DB"),
	collection=os.environ.get("MONGO_CACHE_COLLECTION")
)

mongo_cache_collection = mongo_connect.connect(
	mongo_config=mongo_cache_config)
