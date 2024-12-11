import os
from dotenv import load_dotenv
import mongoengine as me


def connect_to_mongodb():
    load_dotenv()
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
    MONGO_HOST = os.getenv('MONGO_HOST')

    me.connect('quotes_db', host=f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/quotes_db?retryWrites=true&w=majority')
