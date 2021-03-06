from functools import wraps
from turtle import shape

from graphviz import Digraph

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse

from game_book.book import models


def on_progress(view):
    @wraps(view)
    def inner(request, book_id, **kwargs):
        try:
            progress = models.BookProgress.objects.get(book=book_id, user=request.user)
        except models.BookProgress.DoesNotExist:
            return redirect(reverse('book', kwargs={'book_id': book_id}))
        
        return view(request=request, progress=progress, book_id=book_id, **kwargs)
    
    return inner


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


@on_progress
def page(request, progress, book_id, page_id):
    page = get_object_or_404(models.BookPage, book__id=book_id, id=page_id,)

    progress.book_page = page
    progress.save()

    links = [
        (link, link.has_all_needed(list(progress.items.all())))
        for link in page.pagelink_set.all()
    ]

    return render(request, 'page.html', context={
        'page': page,
        'progress': progress,
        'links': links,
        'page_items': page.items.exclude(id__in=progress.items.only('id')),
    })


@on_progress
def take(request, progress, book_id, page_id, item_id):
    item = get_object_or_404(models.Item, id=item_id)

    progress.items.add(item)

    return redirect(reverse('page', kwargs={
        'book_id': book_id, 'page_id': page_id
    }))


def view_book_map(request, book_id):
    book = get_object_or_404(models.Book, id=book_id)

    g = Digraph('Map', filename='map.gv', directory='/tmp')

    def pid(page):
        return f'page_{page.id}'
    
    for page in book.bookpage_set.all():
        g.node(pid(page), label='\n'.join(
            [str(page.id), page.title] + [
                i.name for i in page.items.all()
            ]),
            tooltip=page.body,
            href=f'/admin/book/bookpage/{page.id}/change',
        )

    for link in models.PageLink.objects.filter(from_page__book_id=book_id).all():
        g.edge(pid(link.from_page), pid(link.to_page), label='\n'.join(
            [str(link.id), link.name[:10]] + [
                i.name for i in link.items.all()
            ]),
            labeltooltip=link.name,
            labelhref=f'/admin/book/pagelink/{link.id}/change',
        )
    
    g.render(quiet=True, view=False, format='svg')
    return FileResponse(open('/tmp/map.gv.svg', 'rb'))
