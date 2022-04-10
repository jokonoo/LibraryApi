from rest_framework import serializers

from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name']


class BooksSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    pub_date = serializers.StringRelatedField()
    url = serializers.HyperlinkedIdentityField(
        view_name='detailed_api_view',
        lookup_field='pk')

    class Meta:
        model = Book
        fields = ['id',
                  'title',
                  'authors',
                  'pub_date',
                  'ISBN_10',
                  'ISBN_13',
                  'pages_number',
                  'image',
                  'language',
                  'url']
