from django.contrib import admin

from game_book.book import models

admin.site.register(models.Book)
admin.site.register(models.BookPage)
