import os
import mongoengine as me
from src.models.author import Author
from src.models.quote import Quote
from dotenv import load_dotenv

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

me.connect('authors_and_quotes', host=f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/authors_and_quotes?retryWrites=true&w=majority')


def search_quotes_by_author(author_name):
    author = Author.objects(fullname=author_name).first()
    if author:
        quotes = Quote.objects(author=author)
        return quotes
    else:
        return None

# Тест


if __name__ == '__main__':
    print('В БД есть цитаты: J.K. Rowling, Albert Einstein')
    author_name = input("Введите имя автора: ")
    print(f'Ищем цитаты автора {author_name}...')
    quotes = search_quotes_by_author(author_name)

    if quotes:
        print(f'Цитаты автора {author_name}:')
        for quote in quotes:
            print(f'- {quote.quote}')
    else:
        print(f'Цитаты автора {author_name} не найдены.')



