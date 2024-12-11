from mongoengine import Document, ListField, ReferenceField, StringField
from src.models.author import Author


class Quote(Document):
    quote = StringField(required=True)
    author = ReferenceField(Author)
    tags = ListField(StringField())

