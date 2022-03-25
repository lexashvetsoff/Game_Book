from django.urls import path

from game_book.book import views

urlpatterns = [
    path('', views.index),
    path('book/<int:book_id>', views.book, name='book'),
    path('book/<int:book_id>/page/<int:page_id>', views.page, name='page'),
    path('book/<int:book_id>/page/<int:page_id>/take/<int:item_id>', views.take, name='take'),
    path('book/<int:book_id>/map.svg', views.view_book_map)
]
