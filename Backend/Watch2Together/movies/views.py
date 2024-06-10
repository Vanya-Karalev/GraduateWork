from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Film, Room, Message, Favorites
from users.models import CustomUser
import uuid


def get_mainpage(request):
    return render(request, 'index.html')


def get_films(request):
    films = Film.objects.all()
    favorite_films = []
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_films = Favorites.objects.filter(user=user).values_list('film__id', flat=True)

    context = {'films': films,
               'favorite_films': favorite_films}
    return render(request, 'films.html', context)


def get_film_info(request, slug):
    film = get_object_or_404(Film, slug=slug)
    favorite_films = []
    if request.user.is_authenticated:
        user = CustomUser.objects.get(pk=request.user.id)
        favorite_films = Favorites.objects.filter(user=user).values_list('film__id', flat=True)
    context = {'film': film,
               'favorite_films': favorite_films}
    return render(request, 'aboutfilm.html', context)


def CreateRoom(request, film_id):
    film = Film.objects.get(pk=film_id)

    name = str(uuid.uuid4())
    new_room = Room(room_name=name, owner=request.user, film=film)
    new_room.save()
    return redirect('room', room_name=name)


def MessageView(request, room_name):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "room_name": room_name,
        "room": get_room,
        "current_time": get_room.timer,
        "is_paused": get_room.pause
    }
    return render(request, 'room.html', context)


def watch_film(request, slug):
    film = get_object_or_404(Film, slug=slug)
    context = {'film': film}
    return render(request, 'watch.html', context)
