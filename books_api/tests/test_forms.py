from django.test import TestCase
from books_api.models import Book

from books_api.forms import BookCreateForm, AuthorEditForm, DateEditForm


class BookCreateFormTest(TestCase):

    def test_id_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['id'].label is None or form.fields['id'].label == 'ID')

    def test_title_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['title'].label is None or form.fields['title'].label == 'Title')

    def test_ISBN_10_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['ISBN_10'].label is None or form.fields['ISBN_10'].label == 'ISBN 10')

    def test_ISBN_13_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['ISBN_13'].label is None or form.fields['ISBN_13'].label == 'ISBN 13')

    def test_pages_number_field_label(self):
        form = BookCreateForm()
        self.assertTrue(
            form.fields['pages_number'].label is None or form.fields['pages_number'].label == 'Pages number')

    def test_image_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Image')

    def test_language_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['language'].label is None or form.fields['language'].label == 'Language')

    def test_image_field_label(self):
        form = BookCreateForm()
        self.assertTrue(form.fields['image'].label is None or form.fields['image'].label == 'Image')

    def test_book_create_form_same_as_other_object(self):
        book_object = Book.objects.create(id=1)
        form = BookCreateForm(data={'id': book_object.id})
        self.assertFalse(form.is_valid())

    def test_book_create_form_negative_pages_number(self):
        form = BookCreateForm(data={'id': 1, 'pages_number': -1})
        self.assertFalse(form.is_valid())

    def test_book_create_form_pages_number_bool(self):
        form = BookCreateForm(data={'id': 1, 'pages_number': True})
        self.assertFalse(form.is_valid())
        form = BookCreateForm(data={'id': 1, 'pages_number': False})
        self.assertFalse(form.is_valid())

    def test_book_create_form_pages_number_as_string(self):
        form = BookCreateForm(data={'id': 1, 'pages_number': 'something'})
        self.assertFalse(form.is_valid())

    def test_no_title(self):
        form = BookCreateForm(data={'id': 1})
        self.assertFalse(form.is_valid())

    def test_title_longer_than_250_chars(self):
        form = BookCreateForm(data={'id': 1, 'title': 251*'n'})
        self.assertFalse(form.is_valid())


class AuthorEditFormTest(TestCase):

    def test_title_field_label(self):
        form = AuthorEditForm()
        self.assertTrue(form.fields['authors'].label is None or form.fields['authors'].label == 'Authors')

    def test_no_authors(self):
        form = AuthorEditForm(data={'authors': []})
        self.assertTrue(form.is_valid())

    def test_bool_invalid_false(self):
        form = AuthorEditForm(data={'authors': [False]})
        self.assertFalse(form.is_valid())

    def test_bool_invalid_true(self):
        form = AuthorEditForm(data={'authors': [True]})
        self.assertFalse(form.is_valid())


class DateEditFormTest(TestCase):

    def test_year_field_label(self):
        form = DateEditForm()
        self.assertTrue(form.fields['year'].label is None or form.fields['year'].label == 'Year')

    def test_month_field_label(self):
        form = DateEditForm()
        self.assertTrue(form.fields['month'].label is None or form.fields['month'].label == 'Month')

    def test_day_field_label(self):
        form = DateEditForm()
        self.assertTrue(form.fields['day'].label is None or form.fields['day'].label == 'Day')

    def test_negative_year(self):
        form = DateEditForm(data={'year': -2012})
        self.assertFalse(form.is_valid())

    def test_negative_month(self):
        form = DateEditForm(data={'year': 2012, 'month': -7})
        self.assertFalse(form.is_valid())

    def test_0_month(self):
        form = DateEditForm(data={'year': 2012, 'month': 0})
        self.assertFalse(form.is_valid())

    def test_negative_day(self):
        form = DateEditForm(data={'year': 2012, 'month': 11, 'day': -7})
        self.assertFalse(form.is_valid())

    def test_0_day(self):
        form = DateEditForm(data={'year': 2012, 'month': 11, 'day': 0})
        self.assertFalse(form.is_valid())

    def test_month_out_of_range(self):
        form = DateEditForm(data={'year': 2012, 'month': 13})
        self.assertFalse(form.is_valid())

    def test_day_out_of_range(self):
        form = DateEditForm(data={'year': 2012, 'month': 11, 'day': 32})
        self.assertFalse(form.is_valid())

    def test_month_is_zero(self):
        form = DateEditForm(data={'year': 2012, 'month': 0, 'day': 13})
        self.assertFalse(form.is_valid())

    def test_day_is_zero(self):
        form = DateEditForm(data={'year': 2012, 'month': 2, 'day': 0})
        self.assertFalse(form.is_valid())

    def test_day_without_month(self):
        form = DateEditForm(data={'year': 2012, 'day': 7})
        self.assertFalse(form.is_valid())