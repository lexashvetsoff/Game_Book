from django.urls import path

from game_book.book import views

urlpatterns = [
    path('', views.index),
    path('book/<int:book_id>', views.book),
]