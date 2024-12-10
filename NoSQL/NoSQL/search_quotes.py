import mongoengine as me
from models import Author, Quote

MONGO_USER = os.getenv('MONGO_USER') 
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD') 
MONGO_HOST = os.getenv('MONGO_HOST') 
me.connect('contacts_db', host=f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/contacts_db?retryWrites=true&w=majority'

def search_by_author(name):
    author = Author.objects(fullname=name).first()
    if author:
        quotes = Quote.objects(author=author)
        for quote in quotes:
            print(f"{quote.quote}")
    else:
        print("Author not found.")


def search_by_tag(tag):
    quotes = Quote.objects(tags=tag)
    for quote in quotes:
        print(f"{quote.quote}")


def search_by_tags(tags):
    tag_list = tags.split(',')
    quotes = Quote.objects(tags__in=tag_list)
    for quote in quotes:
        print(f"{quote.quote}")


if __name__ == '__main__':
    while True:
        command = input("Enter command (name:author | tag:tag | tags:tag1,tag2 | exit): ")
        if command.startswith("name:"):
            name = command.split(":", 1)[1].strip()
            search_by_author(name)
        elif command.startswith("tag:"):
            tag = command.split(":", 1)[1].strip()
            search_by_tag(tag)
        elif command.startswith("tags:"):
            tags = command.split(":", 1)[1].strip()
            search_by_tags(tags)
        elif command == "exit":
            break
        else:
            print("Invalid command.")


