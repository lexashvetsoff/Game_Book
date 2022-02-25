from unicodedata import name
from django.db import models

class Book(models.Model):
    '''Interactive function'''
    title = models.TextField(
        name='title',
        unique=True,
    )

    def __str__(self):
        return f'{self.title} ({self.id})'


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

    def __str__(self):
        return f'{self.title} ({self.id})'


class PageLink(models.Model):
    from_page = models.ForeignKey(
        BookPage,
        on_delete=models.CASCADE,
    )

    to_page = models.ForeignKey(
        BookPage,
        related_name='to_page',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.from_page.title} U+1F812 ({self.id})'

    class Meta:
        unique_together = ['from_page', 'to_page']