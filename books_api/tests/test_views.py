import requests

from django.test import TestCase
from django.urls import reverse

from books_api.models import Book, Date, Author


class MainPageBooksListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_books = 15
        for author_id in range(number_of_books):
            if author_id % 2 == 0:
                Book.objects.create(title='hobbit', id=author_id, language='en')
            else:
                Book.objects.create(title='potter', id=author_id, language='pl')

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

    def test_form_get_right_books(self):
        books = list(Book.objects.filter(title__icontains='hobbit'))
        response = self.client.get('/books/?q=hobbit')
        self.assertEqual(books, response.context['page'].object_list)

    def test_form_get_right_books2(self):
        books = list(Book.objects.filter(title__icontains='potter'))
        response = self.client.post('/books/?q=potter')
        self.assertEqual(books, response.context['page'].object_list)


class SavingImportedDatesTest(TestCase):

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

    def test_checking_correct_ids(self):
        response = self.client.post(reverse('book_import_form_view'), data={'?q=': 'hobbit'})
        self.assertEqual(response.status_code, 302)
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes/?q=hobbit').json()
        for item in r.get('items'):
            pub_object = Book.objects.get(id=str(item.get('id'))).id
            self.assertEqual(item.get('id'), pub_object)

    def test_checking_correct_authors(self):
        response = self.client.post(reverse('book_import_form_view'), data={'?q=': 'hobbit'})
        self.assertEqual(response.status_code, 302)
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes/?q=hobbit').json()
        for item in r.get('items'):
            pub_object = [str(author) for author in Book.objects.get(id=str(item.get('id'))).authors.all()]
            self.assertEqual(item.get('volumeInfo').get('authors'), pub_object if pub_object else None)

    def test_checking_correct_authors2(self):
        response = self.client.post(reverse('book_import_form_view'), data={'?q=': 'something'})
        self.assertEqual(response.status_code, 302)
        r = requests.get(f'https://www.googleapis.com/books/v1/volumes/?q=something').json()
        for item in r.get('items'):
            pub_object = [str(author) for author in Book.objects.get(id=str(item.get('id'))).authors.all()]
            self.assertEqual(item.get('volumeInfo').get('authors'), pub_object if pub_object else None)


class EditBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        author_first = Author.objects.create(name='Jan Sobieski')
        author_second = Author.objects.create(name='John Smith')
        date_obj = Date.objects.create(year=2017)
        book_object = Book.objects.create(id='testing123', title='Test123', pub_date=date_obj, ISBN_10='Testing_10',
                                          ISBN_13='Testing_13', pages_number=216, language='TEST')
        book_object.authors.add(author_first, author_second)
        book_object.save()

    def test_view_url_is_correct(self):
        response = self.client.get('/books/edit/testing123/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_reverse_correct(self):
        response = self.client.get(
            reverse('books_detail_view', kwargs={'identifier': Book.objects.get(id='testing123').id}))
        self.assertEqual(response.status_code, 200)

    def test_view_using_correct_template(self):
        response = self.client.get(
            reverse('edit_book_view', kwargs={'identifier': Book.objects.get(id='testing123').id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_api/book_edit.html')

    def test_view_incorrect_identifier(self):
        response = self.client.get(
            reverse('edit_book_view', kwargs={'identifier': 'NotExistingID'}))
        self.assertEqual(response.status_code, 404)

    def test_view_book_form_fields_initial(self):
        book_object = Book.objects.get(id='testing123')
        response = self.client.get(
            reverse('edit_book_view', kwargs={'identifier': book_object.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_b'].initial['title'], book_object.title)
        self.assertEqual(response.context['form_b'].initial['ISBN_10'], book_object.ISBN_10)
        self.assertEqual(response.context['form_b'].initial['ISBN_13'], book_object.ISBN_13)
        self.assertEqual(response.context['form_b'].initial['pages_number'], book_object.pages_number)
        self.assertEqual(response.context['form_b'].initial['language'], book_object.language)

    def test_view_date_form_fields_initial(self):
        book_object = Book.objects.get(id='testing123')
        response = self.client.get(
            reverse('edit_book_view', kwargs={'identifier': book_object.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_d'].initial['year'], book_object.pub_date.year)
        self.assertEqual(response.context['form_d'].initial['month'], book_object.pub_date.month)
        self.assertEqual(response.context['form_d'].initial['day'], book_object.pub_date.day)

    def test_view_author_form_fields_initial(self):
        book_object = Book.objects.get(id='testing123')
        response = self.client.get(
            reverse('edit_book_view', kwargs={'identifier': book_object.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form_a'].initial['authors'], list(book_object.authors.all()))

    def test_redirect_if_success(self):
        book_object = Book.objects.get(id='testing123')
        response = self.client.post(reverse('edit_book_view', kwargs={'identifier': book_object.id}),
                                    {'title': 'new', 'year': 2016})
        self.assertRedirects(response, reverse('books_view'))


class CreateBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        date_obj = Date.objects.create(year=2017)
        Book.objects.create(id='Testing123', pub_date=date_obj)

    def test_view_url_is_correct(self):
        response = self.client.get('/books/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_reverse_correct(self):
        response = self.client.get(reverse('create_book_view'))
        self.assertEqual(response.status_code, 200)

    def test_view_using_correct_template(self):
        response = self.client.get(reverse('create_book_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'books_api/book_add.html')

    def test_form_no_id_passed(self):
        response = self.client.post(reverse('create_book_view'), {'year': 2016})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_b', 'id', 'This field is required.')

    def test_form_not_unique_id(self):
        book_object = Book.objects.get(id='Testing123')
        response = self.client.post(reverse('create_book_view'), {'id': book_object.id, 'year': 2016})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_b', 'id', 'Book with this ID already exists.')

    def test_form_month_higher_than_12(self):
        response = self.client.post(reverse('create_book_view'), {'id': 'new', 'year': 2016, 'month': 13})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_d', 'month', 'Ensure this value is less than or equal to 12.')

    def test_form_month_lower_than_1(self):
        response = self.client.post(reverse('create_book_view'), {'id': 'new', 'year': 2016, 'month': 0})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_d', 'month', 'Ensure this value is greater than or equal to 1.')

    def test_form_day_higher_than_31(self):
        response = self.client.post(reverse('create_book_view'), {'id': 'new', 'year': 2016, 'month': 11, 'day': 32})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_d', 'day', 'Ensure this value is less than or equal to 31.')

    def test_form_day_lower_than_1(self):
        response = self.client.post(reverse('create_book_view'), {'id': 'new', 'year': 2016, 'month': 1, 'day': 0})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form_d', 'day', 'Ensure this value is greater than or equal to 1.')


class DetailBookViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        date_obj = Date.objects.create(year=2017)
        Book.objects.create(id='Testing123', pub_date=date_obj)

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

    def test_view_incorrect_identifier(self):
        response = self.client.get(
            reverse('books_detail_view', kwargs={'identifier': 'NotExistingID'}))
        self.assertEqual(response.status_code, 404)
