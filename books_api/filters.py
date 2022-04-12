from django_filters import rest_framework as filters

from .models import Book, Author


class BookFilter(filters.FilterSet):
    LANGUAGE_CHOICES = [(value, value) for value in Book.objects.values_list('language', flat=True).distinct() if value]
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='authors__name', lookup_expr='icontains')
    pub_date = filters.DateFromToRangeFilter(field_name='pub_date__searching_date')
    authors = filters.ModelMultipleChoiceFilter(field_name='authors__name', to_field_name='name',
                                                queryset=Author.objects.all())
    language = filters.MultipleChoiceFilter(field_name='language', choices=LANGUAGE_CHOICES)

    class Meta:
        model = Book
        fields = ['title', 'pub_date', 'author', 'language']
