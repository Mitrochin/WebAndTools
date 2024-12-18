import os
from bson import ObjectId
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import django
from django.db.utils import IntegrityError
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes.settings')
django.setup()

from quotes_app.models import Author, Quote
from django.contrib.auth.models import User

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

uri = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/authors_and_quotes?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)


def convert_oid(data):
    if isinstance(data, list):
        return [convert_oid(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_oid(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


def convert_date(date_str):
    if date_str:
        for fmt in ('%B %d, %Y', '%Y-%m-%d', '%b %d, %Y'):  # Поддержка нескольких форматов
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
            except ValueError:
                continue
    return None

mongo_db = client['authors_and_quotes']

try:
    authors = mongo_db.get_collection('author').find({})
    authors_list = convert_oid(list(authors))
    if authors_list:
        print(f"Found {len(authors_list)} authors.")
    else:
        print("No authors found in MongoDB.")
except Exception as e:
    print(f"Error accessing author collection: {e}")
    authors_list = []

try:
    quotes = mongo_db.get_collection('quote').find({})
    quotes_list = convert_oid(list(quotes))
    if quotes_list:
        print(f"Found {len(quotes_list)} quotes.")
    else:
        print("No quotes found in MongoDB.")
except Exception as e:
    print(f"Error accessing quote collection: {e}")
    quotes_list = []

author_dict = {author["_id"]: author["fullname"] for author in authors_list}
author_dict.update({author["fullname"]: author["fullname"] for author in authors_list})

for author_data in authors_list:
    try:
        born_date = convert_date(author_data.get('born_date'))
        if not born_date:
            print(f"Skipping author {author_data.get('fullname')} due to invalid date format.")
            continue
        Author.objects.get_or_create(
            fullname=author_data.get('fullname'),
            defaults={
                'born_date': born_date,
                'born_location': author_data.get('born_location'),
                'description': author_data.get('description')
            }
        )
        print(f"Author {author_data.get('fullname')} created successfully.")
    except IntegrityError as e:
        print(f"Error creating author {author_data.get('fullname')}: {e}")

for quote_data in quotes_list:
    try:
        author_id = quote_data.get('author')
        author_fullname = author_dict.get(author_id)

        author = Author.objects.get(fullname=author_fullname)
        Quote.objects.get_or_create(
            quote=quote_data.get('quote'),
            author=author,
            tags=quote_data.get('tags'),
            user=User.objects.first()
        )
        print(f"Quote '{quote_data.get('quote')}' created successfully.")
    except Author.DoesNotExist:
        print(f"Author {author_fullname} not found for quote: {quote_data.get('quote')}")
    except IntegrityError as e:
        print(f"Error creating quote: {quote_data.get('quote')}: {e}")

print("Data migration to PostgreSQL completed successfully!")




















