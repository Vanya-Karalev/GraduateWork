from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Film, Room, Message


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


def CreateRoom(request):
    if request.method == 'POST':
        new_room = Room(owner=request.user)
        new_room.save()
        return redirect('room', room_name=new_room.room_name)
    return render(request, 'message.html')


def MessageView(request, room_name):
    room = get_object_or_404(Room, room_name=room_name)
    messages = Message.objects.filter(room=room_name)
    context = {'room': room,
               'messages': messages}
    return render(request, 'message.html', context)
