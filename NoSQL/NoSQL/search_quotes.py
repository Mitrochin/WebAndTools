import mongoengine as me
from models import Author, Quote

me.connect('authors_and_quotes', host='mongodb+srv://mitrochin:t2oqOReYFZdRRnc2@cluster0.wur7t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')


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


