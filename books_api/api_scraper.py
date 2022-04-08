import requests

from .models import Date, Book, Author


def api_data_scraper():
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
    r = r.json().get('items')
    for item in r:
        volume_data = item.get('volumeInfo')
        book_obj, created = Book.objects.update_or_create(
            id=item.get('id'), defaults={
                'id': item.get('id'),
                'title': volume_data.get('title'),
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
            date = ['year', 'month', 'day']
            pub_date = list(map(int, pub_date.split('-')))
            pub_date = dict(zip(date, pub_date))
            date_obj, created = Date.objects.get_or_create(**pub_date)
            book_obj.pub_date = date_obj
            book_obj.save()

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
