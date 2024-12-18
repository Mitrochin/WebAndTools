from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    fullname = models.CharField(max_length=255, unique=True)
    born_date = models.DateField()
    born_location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.fullname


class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.quote


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



