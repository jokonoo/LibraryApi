from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect

from .api_scraper import api_data_scraper
from .models import Book


def main_page_view(request):
    if params := request.GET:
        context = {'books': Book.objects.all(), 'q': params}
    else:
        context = {'books': Book.objects.all()}
    return render(request, 'books_api/main.html', context)


def detail_book_view(request, identifier):
    book = get_object_or_404(Book, id=identifier)
    return render(request, 'books_api/book.html', {'book': book})


def scraper(request):
    api_data_scraper()
    return HttpResponseRedirect(reverse('books_view'))
