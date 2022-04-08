from datetime import date

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import HttpRequest, HttpResponse

from .api_scraper import api_data_scraper
from .models import Book, Date, Author
from .forms import BookEditForm, DateEditForm, AuthorEditForm


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


def detail_book_view(request: HttpRequest, identifier: str) -> HttpResponse:
    book = get_object_or_404(Book, id=identifier)
    return render(request, 'books_api/book.html', {'book': book})


def edit_book_view(request, identifier: str):
    book = get_object_or_404(Book, id=identifier)
    if request.method == 'POST':
        form_b = BookEditForm(request.POST, instance=book)
        form_d = DateEditForm(request.POST, instance=Date.objects.filter(book__id__exact=book.id)[0])
        form_a = AuthorEditForm(request.POST, instance=book)
        if form_b.is_valid() and form_d.is_valid() and form_a.is_valid():
            form_b.save()
            form_d.save()
            form_a.save()
            return redirect('books_view')
    form_b = BookEditForm(instance=book)
    form_d = DateEditForm(instance=Date.objects.filter(book__id__exact=book.id)[0])
    form_a = AuthorEditForm(instance=book)
    return render(request, 'books_api/test_edit.html',
                  {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})


def create_book_view(request):
    form_b = BookEditForm()
    form_d = DateEditForm()
    form_a = AuthorEditForm()
    return render(request, 'books_api/book_add.html',
                  {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})


def scraper(request):
    api_data_scraper()
    return HttpResponseRedirect(reverse('books_view'))
