import django_filters
from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    pub_date = filters.DateFromToRangeFilter(field_name='pub_date__searching_date')

    class Meta:
        model = Book
        fields = ['title']