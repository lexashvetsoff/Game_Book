from django.shortcuts import render

def index(request):
    return render(request, 'book_index.html', context={
        'who': 'World',
    })