from unicodedata import name
from django.db import models

class Book(models.Model):
    '''Interactive function'''
    title = models.TextField(
        name='title',
        unique=True,
    )
