import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

load_dotenv()

client: MongoClient = MongoClient( # type: ignore
                    os.getenv('MONGO_URI'),
                    server_api = ServerApi('1'))

db = client.pets  # type: ignore

if __name__ == '__main__':
    cursor = list(db.cats.find({})) # type: ignore
    print(cursor) # type: ignore

