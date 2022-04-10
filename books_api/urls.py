from django.urls import path
from .views import main_page_view, scraper, detail_book_view, edit_book_view, create_book_view, BookRemoveView, books_import_form_view

urlpatterns = [
    path('', main_page_view, name='books_view'),
    path('scraping/', scraper, name='scraper'),
    path('create/', create_book_view, name='create_book_view'),
    path('delete/<str:pk>/', BookRemoveView.as_view(), name='book_delete_view'),
    path('details/<str:identifier>/', detail_book_view, name='books_detail_view'),
    path('edit/<str:identifier>/', edit_book_view, name='edit_book_view'),
    path('import/', books_import_form_view, name='book_import_form_view'),
    path('import/<str:query>/', scraper, name='book_import_view')
]
