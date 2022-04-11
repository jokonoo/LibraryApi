from django.test import TestCase
from django.urls import reverse

from books_api.models import Book


class MainPageBooksListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_books = 15

        for author_id in range(number_of_books):
            if author_id % 2 == 0:
                Book.objects.create(id=author_id, language='pl')
            else:
                Book.objects.create(id=author_id, language='en')

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

    def test_showing_right_query_with_languages(self):
        response = self.client.post(reverse('books_view'), data={'language': ['pl']})
        self.assertEqual(response.status_code, 200)
        books = Book.objects.filter(response.POST.get('language'))
        self.assertEqual(Book.objects.filter(language='pl'), books)

        # response = self.client.post(reverse('books_view', kwargs={'language': ['en']}))
        # self.assertEqual(response.status_code, 200)
        # books = Book.objects.filter(response.POST.get('language'))
        # self.assertEqual(Book.objects.filter(language='en'), books)
