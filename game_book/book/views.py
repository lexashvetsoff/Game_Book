from django.shortcuts import render, get_object_or_404

from game_book.book import models


def index(request):
    return render(request, 'book_index.html', context={
        'books': models.Book.objects.all(),
    })


def book(request, book_id):
    return render(request, 'book.html', context={
        'book': get_object_or_404(models.Book, id=book_id)
    })


def page(request, book_id, page_id):
    return render(request, 'page.html', context={
        'page': get_object_or_404(models.BookPage, book__id=book_id, id=page_id,),
    })