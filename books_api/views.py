from datetime import date

from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q

from .api_scraper import api_data_scraper
from .models import Book


def main_page_view(request):
    if params := request.POST:
        q = Q(title__icontains=params.get('q')) | Q(authors__name__icontains=params.get('q'))
        if lang := request.POST.getlist('language'):
            if len(lang) > 1:
                for language in lang:
                    q |= Q(language__exact=language)
            else:
                q &= Q(language__exact=lang[0])
        date_from, date_to = params.get('date_from'), params.get('date_to')
        if date_from and date_to:
            date_from = list(map(int, date_from.split('-')))
            date_to = list(map(int, date_to.split('-')))
            q &= Q(pub_date__searching_date__gte=date(*date_from)) & Q(pub_date__searching_date__lte=date(*date_to))
        elif date_from:
            date_from = list(map(int, date_from.split('-')))
            q &= Q(pub_date__searching_date__gte=date(*date_from))
        elif date_to:
            date_to = list(map(int, date_to.split('-')))
            q &= Q(pub_date__searching_date__lte=date(*date_to))
        books = Book.objects.filter(q).distinct()
        context = {'books': books, 'q': params, 'languages': Book.get_languages_list()}
    else:
        context = {'books': Book.objects.all(), 'languages': Book.get_languages_list()}
    return render(request, 'books_api/main.html', context)


def detail_book_view(request, identifier):
    book = get_object_or_404(Book, id=identifier)
    return render(request, 'books_api/book.html', {'book': book})


def scraper(request):
    api_data_scraper()
    return HttpResponseRedirect(reverse('books_view'))
