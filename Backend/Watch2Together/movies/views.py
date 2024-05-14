from django.shortcuts import render, get_object_or_404
from movies.models import Film


def get_mainpage(request):
    return render(request, 'index.html')


def get_films(request):
    films = Film.objects.all()
    context = {'films': films}
    return render(request, 'films.html', context)


def get_film_info(request, slug):
    film = get_object_or_404(Film, slug=slug)
    context = {'film': film}
    return render(request, 'aboutfilm.html', context)
