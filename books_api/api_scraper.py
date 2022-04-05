import requests

r = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
r = r.json().get('items')
for item in r:
    volume_data = item.get('volumeInfo')
    print(f'title: {volume_data["title"]}')
    print(f'authors: {volume_data["authors"]}')
    print(f'published date: {volume_data["publishedDate"]}')
    print(f'ISBN: {volume_data["industryIdentifiers"]}')
    print(f'page count: volume_data.get("pageCount")')
    print(f'language: {volume_data["language"]}')
    print(f'image links: {volume_data.get("imageLinks")}')
    print()

