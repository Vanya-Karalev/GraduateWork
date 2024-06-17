from django.shortcuts import render, get_object_or_404, redirect
from movies.models import *
from users.models import *
from django.db.models import Q
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
    my_friends = Friends.objects.filter(status='friends').filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    get_room_users = RoomUsers.objects.filter(room=get_room)
    context = {
        "messages": get_messages,
        "room_name": room_name,
        "room": get_room,
        "current_time": get_room.timer,
        "is_paused": get_room.pause,
        'friends': my_friends,
        'room_users': get_room_users,
    }
    if (get_room.owner.subscription or get_room.owner.period != 0 and get_room_users.count() < 10) or get_room_users.count() < 2:
        return render(request, 'room.html', context)
    else:
        return render(request, 'error.html')


def watch_film(request, slug):
    film = get_object_or_404(Film, slug=slug)
    context = {'film': film}
    return render(request, 'watch.html', context)


def room_error(request):
    return render(request, 'error.html')
