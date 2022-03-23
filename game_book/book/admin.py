from django.contrib import admin

from game_book.book import models

admin.site.register(models.Book)
admin.site.register(models.BookPage)
admin.site.register(models.PageLink)
admin.site.register(models.BookProgress)
admin.site.register(models.Item)
