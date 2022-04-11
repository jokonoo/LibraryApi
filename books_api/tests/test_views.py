import requests

from django.test import TestCase
from django.urls import reverse

from books_api.models import Book


class MainPageBooksListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_books = 15

        for author_id in range(number_of_books):
            if author_id % 2 == 0:
                Book.objects.create(id=author_id, language='en')
            else:
                Book.objects.create(id=author_id, language='pl')

    def test_view_url_is_correct(self):
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_reverse_correct(self):
        response = self.client.get(reverse('books_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_using_correct_template(self):
        response = self.client.get(reverse('books_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_api/main.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('books_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page']), 10)

    def test_pagination_show_correct_books(self):
        response = self.client.get(reverse('books_view') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page' in response.context)
        self.assertEqual(len(response.context['page']), 5)

    def test_showing_right_languages(self):
        response = self.client.get(reverse('books_view'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(sorted([Book.objects.get(id=1).language, Book.objects.get(id=2).language]),
                         response.context['languages'])


class SavingImportedDatesTest(TestCase):

    def setUp(self):
        self.client.post(reverse('book_import_form_view'), data={'?q=': 'hobbit'})

    def test_checking_correct_dates(self):
        response = self.client.post(reverse('book_import_form_view'), data={'?q=': 'hobbit'})
        self.assertEqual(response.status_code, 302)
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes/?q=hobbit').json()
        for item in r.get('items'):
            pub_object = Book.objects.get(id=str(item.get('id'))).pub_date.get_full_date()
            date_str = item.get('volumeInfo').get('publishedDate')
            pub_date = '-'.join(list(map(str, list(map(int, date_str.split('-'))))))
            self.assertEqual(pub_date, pub_object)

    def test_checking_correct_dates2(self):

        response = self.client.post(reverse('book_import_form_view'), data={'?q=': 'something'})
        self.assertEqual(response.status_code, 302)
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes/?q=something').json()
        for item in r.get('items'):
            pub_object = Book.objects.get(id=str(item.get('id'))).pub_date.get_full_date()
            date_str = item.get('volumeInfo').get('publishedDate')
            pub_date = '-'.join(list(map(str, list(map(int, date_str.split('-'))))))
            self.assertEqual(pub_date, pub_object)


class EditBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Book.objects.create(id='Testing123')

    def test_view_url_is_correct(self):
        response = self.client.get('/books/details/Testing123/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_reverse_correct(self):
        response = self.client.get(
            reverse('books_detail_view', kwargs={'identifier': Book.objects.get(id='Testing123').id}))
        self.assertEqual(response.status_code, 200)

    def test_view_using_correct_template(self):
        response = self.client.get(
            reverse('books_detail_view', kwargs={'identifier': Book.objects.get(id='Testing123').id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_api/book.html')


class CreateBookView(TestCase):
    pass


class DetailBookViewTest(TestCase):
    pass
