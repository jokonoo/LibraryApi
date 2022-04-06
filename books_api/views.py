from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from .api_scraper import api_data_scraper


def main_page_view(request):
    return render(request, 'books_api/main.html')


def scraper(request):
    api_data_scraper()
    return HttpResponseRedirect(reverse('main'))

