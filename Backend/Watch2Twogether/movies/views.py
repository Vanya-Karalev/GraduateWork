from django.shortcuts import render


def get_mainpage(request):
    return render(request, 'index.html')


def get_films(request):
    return render(request, 'films.html')
