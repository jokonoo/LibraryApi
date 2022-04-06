from django.urls import path
from .views import main_page_view, scraper

urlpatterns = [
    path('', main_page_view, name='main'),
    path('scraping', scraper, name='scraper')
]
