from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(
        name='title',
        max_length=100,
        unique=True,
    )

    first_page = models.ForeignKey(
        'BookPage',
        null=True,
        on_delete=models.SET_NULL,
        related_name='first_page',
    )

    cover_art = models.ImageField(
        null=True,
    )

    def __str__(self):
        return f'{self.title} ({self.id})'


class BookPage(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        name='title',
        max_length=100,
    )

    body = models.TextField(
        name='body',
    )

    items = models.ManyToManyField('book.Item', blank=True)

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

    name = models.TextField()

    items = models.ManyToManyField('book.Item', blank=True)

    class Meta:
        unique_together = ['from_page', 'to_page']

    def __str__(self):
        return f'{self.from_page.title} -> {self.to_page.title} ({self.id})'

    def has_all_needed(self, items):
        return all(i in items for i in self.items.all())


class BookProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    book_page = models.ForeignKey(
        BookPage,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField('book.Item', blank=True)

    class Meta:
        unique_together = ['user', 'book']
    
    @classmethod
    def start_reading(cls, user, book):
        progress = BookProgress(user=user, book=book, book_page=book.first_page)
        progress.save()
        return progress


class Item(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.name}'