from unicodedata import name
from django.db import models

class Book(models.Model):
    '''Interactive function'''
    title = models.TextField(
        name='title',
        unique=True,
    )

class BookPage(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    title = models.TextField(
        name='title',
    )

    body = models.TextField(
        name='body',
    )