import requests

from .models import Date, Book, Author

r = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
r = r.json().get('items')
for item in r:
    volume_data = item.get('volumeInfo')
    obj, created = Book.objects.update_or_create(
        id=item.get('id'), defaults={
            'id': item.get('id'),
            'title': volume_data.get('title'),
            'pages_number': volume_data.get('pageCount'),
            'language': volume_data.get('language')
        })
    if authors := volume_data.get('authors'):
        for author in authors:
            author_obj, created = Author.objects.get_or_create(name=author)
            obj.authors.add(author_obj)
    print(f'title: {volume_data["title"]}')
    print(f'authors: {volume_data["authors"]}')
    print(f'published date: {volume_data["publishedDate"]}')
    print(f'ISBN: {volume_data["industryIdentifiers"]}')
    print(f'page count: volume_data.get("pageCount")')
    print(f'language: {volume_data["language"]}')
    print(f'image links: {volume_data.get("imageLinks")}')
    print()
