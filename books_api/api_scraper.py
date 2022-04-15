from itertools import zip_longest
import requests

from django.core.exceptions import MultipleObjectsReturned
from django.db import DataError
from django.db.models import Q

from .models import Date, Book, Author


def api_data_scraper(values):
    url = f'https://www.googleapis.com/books/v1/volumes/'

    for key, value in values.items():
        if value:
            url += f'{key}{value}'
    r = requests.get(url).json()

    if r.get('items'):
        for item in r.get('items'):
            try:
                volume_data = item.get('volumeInfo')
                book_obj, created = Book.objects.update_or_create(
                    id=item.get('id'), defaults={
                        'id': item.get('id'),
                        'title': volume_data.get('title').strip if volume_data.get('title') else volume_data.get(
                            'title'),
                        'pages_number': volume_data.get('pageCount'),
                        'language': volume_data.get('language')
                    })

                if authors := volume_data.get('authors'):
                    if not created:
                        book_obj.authors.clear()
                    for author in authors:
                        author_obj, created = Author.objects.get_or_create(name=author)
                        book_obj.authors.add(author_obj)

                if pub_date := volume_data.get('publishedDate'):
                    try:
                        dates = ['year', 'month', 'day']
                        pub_date = list(map(int, pub_date.split('-')))
                        pub_date_dict_alt = dict(zip_longest(dates, pub_date))
                        try:
                            if not all(value for value in pub_date_dict_alt.values()):
                                raise MultipleObjectsReturned
                            pub_date_dict = dict(zip(dates, pub_date))
                            date_obj, created = Date.objects.get_or_create(**pub_date_dict)
                            book_obj.pub_date = date_obj
                            book_obj.save()
                        except MultipleObjectsReturned:
                            pub_date_dict = dict(zip(dates, pub_date))
                            q = Q()
                            for key, value in pub_date_dict_alt.items():
                                if value:
                                    q &= Q(**{key: value})
                                else:
                                    q &= Q(**{f'{key}__isnull': True})
                            if date_object := Date.objects.filter(q):
                                date_obj = date_object[0]
                                book_obj.pub_date = date_obj
                                book_obj.save()
                            else:
                                date_obj = Date.objects.create(**pub_date_dict)
                                book_obj.pub_date = date_obj
                                book_obj.save()
                    except ValueError:
                        pass

                if identifiers := volume_data.get('industryIdentifiers'):
                    for identifier in identifiers:
                        if identifier.get('type') == 'ISBN_10':
                            book_obj.ISBN_10 = identifier.get('identifier')
                            book_obj.save()
                        if identifier.get('type') == 'ISBN_13':
                            book_obj.ISBN_13 = identifier.get('identifier')
                            book_obj.save()

                if thumbnail := volume_data.get('imageLinks'):
                    book_obj.image = thumbnail.get('thumbnail')
                    book_obj.save()
            except DataError:
                pass
