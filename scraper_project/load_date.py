import os
from dotenv import load_dotenv
import json
import mongoengine as me
from src.models.author import Author
from src.models.quote import Quote

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

me.connect('authors_and_quotes', host=f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/authors_and_quotes?retryWrites=true&w=majority')


def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(
                fullname=author_data['fullname'],
                born_date=author_data['born_date'],
                born_location=author_data['born_location'],
                description=author_data['description']
            )
            author.save()
    print("Authors data loaded successfully.")


def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            quote = Quote(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()
    print("Quotes data loaded successfully.")


if __name__ == '__main__':
    load_authors('data/authors.json')
    load_quotes('data/quotes.json')
    print("Data loaded successfully.")



