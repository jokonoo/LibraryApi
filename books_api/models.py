from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.shortcuts import reverse


class Date(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True, validators=[
            MaxValueValidator(12),
            MinValueValidator(1)])
    day = models.IntegerField(blank=True, null=True, validators=[
            MaxValueValidator(31),
            MinValueValidator(1)])
    searching_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.searching_date = date(self.year, self.month or 1, self.day or 1)
        super().save(*args, **kwargs)

    def get_full_date(self, separator='-'):
        if self.month and self.day:
            return f'{self.year}-{self.month}-{self.day}'
        elif self.month:
            return f'{self.year}-{self.month}'
        else:
            return f'{self.year}'

        #return_date = str(self.year)
        #return_date += separator + str(self.month) if self.month else return_date
        #return_date += separator + st(self.day) if self.day else return_date
        #return return_date

    def __str__(self):
        return self.get_full_date()


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class Book(models.Model):
    id = models.CharField(max_length=200, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.ForeignKey(Date, on_delete=models.SET_NULL, blank=True, null=True)
    ISBN_10 = models.CharField(max_length=200, blank=True, null=True)
    ISBN_13 = models.CharField(max_length=200, blank=True, null=True)
    pages_number = models.IntegerField(blank=True, null=True)
    image = models.URLField(max_length=250, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return f'ID:{self.id}, Title:{self.title}'

    def get_authors_names(self):
        if authors := self.authors.all():
            return [author.name for author in authors]

    def get_absolute_url(self):
        return reverse('books_detail_view', kwargs={'identifier': self.id})

    @staticmethod
    def get_languages_list():
        languages = list(Book.objects.values_list('language').distinct())
        return [language[0] for language in languages]

