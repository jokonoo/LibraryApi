from django.db import models
from django.shortcuts import reverse


class Date(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    def get_full_date(self):
        if self.month and self.day:
            return f'{self.year}-{self.month}-{self.day}'
        elif self.month:
            return f'{self.year}-{self.month}'
        else:
            return f'{self.year}'

    def __str__(self):
        return self.get_full_date()


class Book(models.Model):
    id = models.CharField(max_length=200, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.ForeignKey(Date, on_delete=models.SET_NULL, blank=True, null=True)
    ISBN_10 = models.CharField(max_length=200, blank=True, null=True)
    ISBN_13 = models.CharField(max_length=200, blank=True, null=True)
    pages_number = models.IntegerField(blank=True, null=True)
    image = models.URLField(max_length=250, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'ID:{self.id}, Title:{self.title}'

    def get_authors_names(self):
        if authors := self.authors.all():
            return [author.name for author in authors]

    def get_absolute_url(self):
        return reverse('books_detail_view', kwargs={'identifier': self.id})


class Author(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='authors')

    def __str__(self):
        return f'{self.name}'

