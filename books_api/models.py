from django.db import models


class Date(models.Model):
    year = models.IntegerField()
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)


class Book(models.Model):
    id = models.CharField(max_length=200, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=200, blank=True)
    pub_date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    ISBN_10 = models.IntegerField(blank=True, null=True)
    ISBN_13 = models.IntegerField(blank=True, null=True)
    pages_number = models.IntegerField(blank=True, null=True)
    image = models.URLField(max_length=250, blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)


class Author(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name='authors')
