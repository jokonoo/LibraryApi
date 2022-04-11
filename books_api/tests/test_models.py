from datetime import date

from django.test import TestCase

from books_api.models import Book, Author, Date


class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        book_object = Book.objects.create(id='TEST', title="Testing 1 2 3 Testing",
                                          pub_date=Date.objects.create(year=2015, month=10, day=31), ISBN_10='TEST',
                                          ISBN_13='TEST',
                                          pages_number=315, image='http://www.testing.com', language='en')
        author = Author.objects.create(name='TestingAuthor123')
        book_object.authors.add(author)

        Book.objects.create(id='TEST2', language='pl')

    def test_id_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'ID')

    def test_title_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_pub_date_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'pub date')

    def test_ISBN_10_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('ISBN_10').verbose_name
        self.assertEqual(field_label, 'ISBN 10')

    def test_ISBN_13_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('ISBN_13').verbose_name
        self.assertEqual(field_label, 'ISBN 13')

    def test_pages_number_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('pages_number').verbose_name
        self.assertEqual(field_label, 'pages number')

    def test_image_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('image').verbose_name
        self.assertEqual(field_label, 'image')

    def test_language_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('language').verbose_name
        self.assertEqual(field_label, 'language')

    def test_authors_label(self):
        book = Book.objects.get(id='TEST')
        field_label = book._meta.get_field('authors').verbose_name
        self.assertEqual(field_label, 'authors')

    def test_id_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('id').max_length
        self.assertEqual(max_length, 50)

    def test_title_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_ISBN_10_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('ISBN_10').max_length
        self.assertEqual(max_length, 200)

    def test_ISBN_13_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('ISBN_13').max_length
        self.assertEqual(max_length, 200)

    def test_image_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('image').max_length
        self.assertEqual(max_length, 250)

    def test_language_max_length(self):
        book = Book.objects.get(id='TEST')
        max_length = book._meta.get_field('language').max_length
        self.assertEqual(max_length, 50)

    def test_str_name_is_id_comma_title_coma_date(self):
        book = Book.objects.get(id='TEST')
        expected_book_name = f'ID:{book.id}, Title:{book.title}, Date: {book.pub_date}'
        self.assertEqual(str(book), expected_book_name)

    def test_get_absolute_url(self):
        book = Book.objects.get(id='TEST')
        self.assertEqual(book.get_absolute_url(), '/books/details/TEST/')

    def test_get_authors_names(self):
        book = Book.objects.get(id='TEST')
        author = [book.authors.all()[0].name]
        self.assertEqual(author, book.get_authors_names())

    def test_get_languages_list(self):
        book = Book.objects.get(id='TEST')
        second_book_object = Book.objects.get(id='TEST2')
        languages_list = [book.language, second_book_object.language]
        self.assertEqual(languages_list, Book.get_languages_list())


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Author.objects.create(name='Andrew Garfield')

    def test_name_label(self):
        author_object = Author.objects.get(id=1)
        field_label = author_object._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        author_object = Author.objects.get(id=1)
        max_length = author_object._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_str_name_is_name(self):
        author_object = Author.objects.get(id=1)
        expected_author_name = f'{author_object.name}'
        self.assertEqual(str(author_object), expected_author_name)


class DateModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        date = Date.objects.create(year=2015, month=11, day=30)
        Date.objects.create(year=2016, month=7)
        Date.objects.create(year=2013)

    def test_year_label(self):
        date_object = Date.objects.get(id=2)
        field_label = date_object._meta.get_field('year').verbose_name
        self.assertEqual(field_label, 'year')

    def test_month_label(self):
        date_object = Date.objects.get(id=2)
        field_label = date_object._meta.get_field('month').verbose_name
        self.assertEqual(field_label, 'month')

    def test_day_label(self):
        date_object = Date.objects.get(id=2)
        field_label = date_object._meta.get_field('day').verbose_name
        self.assertEqual(field_label, 'day')

    def test_searching_date_label(self):
        date_object = Date.objects.get(id=2)
        field_label = date_object._meta.get_field('searching_date').verbose_name
        self.assertEqual(field_label, 'searching date')

    def test_get_full_date_with_full_date(self):
        date_object = Date.objects.get(id=2)
        date_object_full_date = f'{date_object.year}-{date_object.month}-{date_object.day}'
        self.assertEqual(date_object_full_date, date_object.get_full_date())

    def test_get_full_date_with_year_and_month(self):
        date_object = Date.objects.get(id=3)
        date_object_full_date = f'{date_object.year}-{date_object.month}'
        self.assertEqual(date_object_full_date, date_object.get_full_date())

    def test_get_full_date_with_year_only(self):
        date_object = Date.objects.get(id=4)
        date_object_full_date = f'{date_object.year}'
        self.assertEqual(date_object_full_date, date_object.get_full_date())

    def test_str_name_if_full_date(self):
        date_object = Date.objects.get(id=2)
        date_object_full_date = f'{date_object.year}-{date_object.month}-{date_object.day}'
        self.assertEqual(date_object_full_date, str(date_object))

    def test_str_name_if_year_and_month(self):
        date_object = Date.objects.get(id=3)
        date_object_full_date = f'{date_object.year}-{date_object.month}'
        self.assertEqual(date_object_full_date, str(date_object))

    def test_str_name_if_year_only(self):
        date_object = Date.objects.get(id=4)
        date_object_full_date = f'{date_object.year}'
        self.assertEqual(date_object_full_date, str(date_object))

    def test_searching_date_if_full_date(self):
        date_object = Date.objects.get(id=2)
        date_object_search_date = date(date_object.year, date_object.month, date_object.day)
        self.assertEqual(date_object_search_date, date_object.searching_date)

    def test_searching_date_if_year_and_month(self):
        date_object = Date.objects.get(id=3)
        date_object_search_date = date(date_object.year, date_object.month, 1)
        self.assertEqual(date_object_search_date, date_object.searching_date)

    def test_searching_date_if_year_only(self):
        date_object = Date.objects.get(id=4)
        date_object_search_date = date(date_object.year, 1, 1)
        self.assertEqual(date_object_search_date, date_object.searching_date)