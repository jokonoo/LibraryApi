from django import forms

from .models import Book, Date


class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'ISBN_10', 'ISBN_13', 'pages_number', 'image', 'language']
        widgets = {
            'title': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'title'}),
            'ISBN_10': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'ISBN_10'}),
            'ISBN_13': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'ISBN_13'}),
            'pages_number': forms.NumberInput(
                attrs={'type': 'number', 'class': 'form-control', 'id': 'pages_number',
                       'placeholder': 'Enter number of pages'}),
            'image': forms.URLInput(
                attrs={'type': 'url', 'class': 'form-control', 'id': 'image'}),
            'language': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'language'}),
        }


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id', 'title', 'ISBN_10', 'ISBN_13', 'pages_number', 'image', 'language']
        widgets = {
            'id': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'id'}),
            'title': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'title'}),
            'ISBN_10': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'ISBN_10'}),
            'ISBN_13': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'ISBN_13'}),
            'pages_number': forms.NumberInput(
                attrs={'type': 'number', 'class': 'form-control', 'id': 'pages_number',
                       'placeholder': 'Enter number of pages'}),
            'image': forms.URLInput(
                attrs={'type': 'url', 'class': 'form-control', 'id': 'image'}),
            'language': forms.TextInput(
                attrs={'type': 'text', 'class': 'form-control', 'id': 'language'}),
        }


class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['authors']
        widgets = {'authors': forms.SelectMultiple(attrs={'class': 'form-select'})}


class DateEditForm(forms.ModelForm):

    class Meta:
        model = Date
        exclude = ('searching_date',)
        widgets = {
            'year': forms.NumberInput(
                attrs={'type': 'number', 'class': 'form-control', 'id': 'year',
                       'placeholder': 'Enter year'}),
            'month': forms.NumberInput(
                attrs={'type': 'number', 'class': 'form-control', 'id': 'month',
                       'placeholder': 'Enter month'}),
            'day': forms.NumberInput(
                attrs={'type': 'number', 'class': 'form-control', 'id': 'day',
                       'placeholder': 'Enter day'})
        }