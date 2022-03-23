from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from game_book.book import models


def index(request):
    return render(request, 'book_index.html', context={
        'books': models.Book.objects.all(),
    })


def book(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)
    if not book.first_page:
        return render(request, 'book.html', context={
        'book': book
        })

    try:
        progress = models.BookProgress.objects.get(book=book, user=request.user)
    except models.BookProgress.DoesNotExist:
        progress = models.BookProgress.start_reading(user=request.user, book=book)

    return redirect(reverse('page', kwargs={
        'book_id': book.id, 'page_id': progress.book_page.id
    }))



def page(request, book_id, page_id):
    # Защита от взлома - доделать надо
    # query = models.BookProgress.objects.filter(book=book_id, user=request.user, book_page=page_id)
    # if not query:
    #     return redirect(reverse('book', kwargs={'book_id': book_id}))
    try:
        progress = models.BookProgress.objects.get(book=book_id, user=request.user)
    except models.BookProgress.DoesNotExist:
        return redirect(reverse('book', kwargs={'book_id': book_id}))

    page = get_object_or_404(models.BookPage, book__id=book_id, id=page_id,)

    progress.book_page = page
    progress.save()

    return render(request, 'page.html', context={
        'page': page,
        'items': progress.items.all(),
    })