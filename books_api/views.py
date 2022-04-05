from django.shortcuts import render


def main_page_view(request):
    return render(request, 'books_api/main.html')
