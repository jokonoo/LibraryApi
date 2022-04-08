from django.urls import path
from .views import main_page_view, scraper, detail_book_view

urlpatterns = [
    path('', main_page_view, name='books_view'),
    #path(),
    path('scraping/', scraper, name='scraper'),
    path('details/<str:identifier>/', detail_book_view, name='books_detail_view'),
]