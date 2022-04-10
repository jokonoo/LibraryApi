from datetime import date

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from rest_framework import generics

from .serializers import BooksSerializer
from .api_scraper import api_data_scraper
from .models import Book, Date, Author
from .forms import BookEditForm, BookCreateForm, DateEditForm, AuthorEditForm


class BooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer


class DetailedBookView(generics.RetrieveAPIView):

    queryset = Book.objects.all()
    serializer_class = BooksSerializer


class BookRemoveView(DeleteView):
    model = Book
    template_name = 'books_api/book_delete.html'
    success_url = reverse_lazy('books_view')


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
            book_object = form_b.save()
            form_d.save()
            form_a.save()
            if author_input := request.POST.get('authorInput'):
                author_input = author_input.split(',')
                for author in author_input:
                    author_object, created = Author.objects.get_or_create(name=author.strip())
                    book_object.authors.add(author_object)
            return redirect('books_view')
        return render(request, 'books_api/test_edit.html',
                      {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})
    form_b = BookEditForm(instance=book)
    form_d = DateEditForm(instance=Date.objects.filter(book__id__exact=book.id)[0])
    form_a = AuthorEditForm(instance=book)
    return render(request, 'books_api/test_edit.html',
                  {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})


def create_book_view(request):
    form_b, form_d, form_a = BookCreateForm(), DateEditForm(), AuthorEditForm()
    if request.method == 'POST':
        form_b, form_d, form_a = BookCreateForm(request.POST), DateEditForm(request.POST), AuthorEditForm(request.POST)
        if form_b.is_valid() and form_d.is_valid() and form_a.is_valid():
            date_object = form_d.save()
            book_object = form_b.save()
            book_object.pub_date = date_object
            if authors := request.POST.getlist('authors'):
                for pk_value in authors:
                    book_object.authors.add(Author.objects.get(pk=int(pk_value)))
            if author_input := request.POST.get('authorInput'):
                author_input = author_input.split(',')
                for author in author_input:
                    author_object, created = Author.objects.get_or_create(name=author.strip())
                    book_object.authors.add(author_object)
            book_object.save()
        return render(request, 'books_api/book_add.html',
                      {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})

    return render(request, 'books_api/book_add.html',
                  {'form_b': form_b, 'form_d': form_d, 'form_a': form_a, 'languages': Book.get_languages_list()})


@csrf_exempt
def books_import_form_view(request):
    if request.method == "POST":
        params_values = request.POST
        api_data_scraper(params_values)
        return HttpResponseRedirect(reverse('books_view'))

    return render(request, 'books_api/book_import.html')
