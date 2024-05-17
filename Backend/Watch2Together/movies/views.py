from django.shortcuts import render, get_object_or_404, redirect
from movies.models import Film, Room, Message
import uuid


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
        # try:
        #     name = str(uuid.uuid4())
        #     print(name)
        #     return redirect('room', room_name=name)
        # except Room.DoesNotExist:
        #     name = str(uuid.uuid4())
        #     print(name)
        #     new_room = Room(room_name=name, owner=request.user)
        #     new_room.save()
        #     return redirect('room', room_name=new_room.room_name)

        name = str(uuid.uuid4())
        new_room = Room(room_name=name, owner=request.user)
        new_room.save()
        return redirect('room', room_name=name)

    return render(request, 'room.html')


def MessageView(request, room_name):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)

    context = {
        "messages": get_messages,
        "room_name": room_name,
    }
    return render(request, 'room.html', context)
