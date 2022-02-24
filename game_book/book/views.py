from django.shortcuts import render, get_object_or_404

from game_book.book.models import Book


def index(request):
    return render(request, 'book_index.html', context={
        'books': Book.objects.all(),
    })


def book(request, book_id):
    return render(request, 'book.html', context={
        'book': get_object_or_404(Book, id=book_id)
    })