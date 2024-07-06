import os

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

# 46 hours
DOCUMENTS_EXPIRE_AFTER_SECONDS = 82800 * 2


def init_db():
    # Initialize the pipeline and connect to the MongoDB client
    # Create a new client and connect to the server
    mongo_client = MongoClient(os.getenv('MONGO_DB_URI'), server_api=ServerApi('1'))
    db = mongo_client[os.getenv('MONGO_DB_NAME')]  # Access the news_db database

    return db


def create_indexes(collection):
    index_list = sorted(list(collection.index_information()))
    digest_index_exists = 'digest_1' in index_list
    created_at_index_exists = 'createdAt_1' in index_list

    if not digest_index_exists:
        collection.create_index("digest", unique=True)

    if not created_at_index_exists:
        document_expire_after_secs = DOCUMENTS_EXPIRE_AFTER_SECONDS
        collection.create_index(
            "createdAt", expireAfterSeconds=document_expire_after_secs, background=True)

    return collection
