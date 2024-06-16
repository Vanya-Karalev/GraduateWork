from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
# from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Friends, Notifications
from movies.models import Film, Favorites, Room
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import check_password, make_password
import re
from django.utils import timezone


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('mainpage')
#     template_name = 'register.html'
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         login(self.request, self.object)
#         return response


def register(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        context['username'] = username
        email = request.POST.get('email')
        context['email'] = email
        password = request.POST.get('password1')
        context['password'] = password
        confirm_password = request.POST.get('password2')
        context['confirm_password'] = confirm_password
        if password == confirm_password:
            if CustomUser.objects.filter(username=username).exists():
                context['error_username'] = 'Такой пользователь уже существует'
            elif not re.match(r'^[a-zA-Z0-9]+$', username):
                context['error_username'] = 'Укажите верный username'
            elif email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                context['error_email'] = 'Укажите верную почту'
            else:
                user = CustomUser.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('mainpage')
        else:
            context['error_password'] = 'Пароли не совпадают'
    return render(request, 'register.html', context)


def update_profile(request):
    context = {}
    user = request.user
    if request.method == 'POST':
        email = request.POST.get('email')
        context['email'] = email
        password = request.POST.get('password1')
        context['password'] = password
        new_password = request.POST.get('password2')
        context['new_password'] = new_password
        image = request.FILES.get('image')

        if check_password(password, user.password) and new_password != '' and password != '':
            user.password = make_password(new_password)
        else:
            context['error_password'] = 'Неверный пароль'

        if email and email != user.email:
            if email == '' or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                context['error_email'] = 'Укажите верную почту'
            else:
                user.email = email

        if image:
            user.image = image

        if not context:
            user.save()
            return redirect('profile')
    return render(request, 'profile.html', context)


# class ProfileView(UpdateView):
#     form_class = CustomUserChangeForm
#     success_url = reverse_lazy('mainpage')
#     template_name = 'profile.html'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def form_valid(self, form):
#         user = form.save()
#         return super().form_valid(form)


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('mainpage')

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('mainpage')


def friends(request):
    all_users = CustomUser.objects.all().exclude(id=request.user.id).exclude(is_superuser=True)

    my_requests = Friends.objects.filter(status='request_sent', sender=request.user)
    my_requests_ids = my_requests.values_list('receiver__id', flat=True)

    for_me_requests = Friends.objects.filter(status='request_sent', receiver=request.user)
    for_me_requests_ids = for_me_requests.values_list('sender__id', flat=True)

    my_friends = Friends.objects.filter(status='friends').filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    friends_ids = my_friends.values_list('receiver__id', flat=True).union(
        my_friends.values_list('sender__id', flat=True)
    )
    non_friends = all_users.exclude(id__in=friends_ids).exclude(id__in=my_requests_ids).exclude(id__in=for_me_requests_ids)

    context = {
        'friends': my_friends,
        'my_requests': my_requests,
        'for_me_requests': for_me_requests,
        'all_users': non_friends
    }

    return render(request, 'friends.html', context)


def add_friend(request, user_id):
    # if request.method == 'POST':
    receiver = get_object_or_404(CustomUser, id=user_id)
    friend_request = Friends(sender=request.user, receiver=receiver, status='request_sent')
    friend_request.save()

    notification = Notifications(
        sender=request.user,
        receiver=receiver,
        text_notification=f"{request.user.username} отправил(а) вам запрос для добавления в друзья.",
        notification_date=timezone.now()
    )
    notification.save()

    return redirect('friends')


def remove_friend(request, friend_id):
    # if request.method == 'POST':
    friend = Friends.objects.filter(id=friend_id, sender_id=request.user).first()
    if not friend:
        friend = Friends.objects.filter(id=friend_id, receiver_id=request.user).first()

    if friend.sender == request.user:
        user_to_remove = get_object_or_404(CustomUser, id=friend.receiver.id)
    else:
        user_to_remove = get_object_or_404(CustomUser, id=friend.sender.id)

    friendship = Friends.objects.filter(
        Q(sender=request.user, receiver=user_to_remove) |
        Q(sender=user_to_remove, receiver=request.user),
        status='friends'
    ).first()

    if friendship:
        friendship.delete()

    return redirect('friends')


def accept_request(request, user_id):
    # if request.method == 'POST':
    sender = get_object_or_404(CustomUser, id=user_id)

    friend_request = get_object_or_404(Friends, sender=sender, receiver=request.user, status='request_sent')

    friend_request.status = 'friends'
    friend_request.save()

    notification = Notifications(
        sender=sender,
        receiver=request.user,
        text_notification=f"{request.user.username} принял(а) ваш запрос в друзья.",
        notification_date=timezone.now()
    )
    notification.save()

    return redirect('friends')


def decline_request(request, user_id):
    # if request.method == 'POST':
    receiver = get_object_or_404(CustomUser, id=user_id)

    friendship = Friends.objects.filter(sender=request.user, receiver=receiver).first()

    if friendship:
        friendship.delete()

    return redirect('friends')


def notifications(request):
    now = timezone.now().isoformat()
    my_notifications = Notifications.objects.filter(receiver=request.user)
    context = {'notifications': my_notifications,
               'now': now}
    return render(request, 'notification.html', context)


def favorite(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    user = request.user

    is_favorite = Favorites.objects.filter(user=user, film=film).exists()

    if is_favorite:
        Favorites.objects.filter(user=user, film=film).delete()
    else:
        Favorites.objects.create(user=user, film=film)

    next_page = request.GET.get('next')
    film_slug = request.GET.get('slug')

    if next_page == 'film_info' and film_slug:
        return redirect('film_info', slug=film_slug)
    elif next_page == 'films':
        return redirect('films')
    elif next_page == 'myfavoritefilms':
        return redirect('myfavoritefilms')
    else:
        return redirect('films')


def my_favorite_films(request):
    user = CustomUser.objects.get(pk=request.user.id)
    films = Film.objects.all()
    favorite_films = Favorites.objects.filter(user=user)
    favoritee_films = Favorites.objects.filter(user=user).values_list('film__id', flat=True)
    context = {'films': films,
               'favorite_films': favorite_films,
               'favoritee_films': favoritee_films}
    return render(request, 'favourites.html', context)


def subscription(request):
    return render(request, 'subscription.html')


def buy_subscription(request, days):
    user = request.user
    user.subscription = True
    user.period = user.period + days
    user.save()
    notification = Notifications(
        sender=request.user,
        receiver=request.user,
        text_notification=f"Вы купили/продлили подписку.",
        notification_date=timezone.now()
    )
    notification.save()
    return redirect('subscription')


def cancel_subscription(request):
    user = request.user
    user.subscription = False
    user.save()
    notification = Notifications(
        sender=request.user,
        receiver=request.user,
        text_notification=f"Вы отменили подписку.",
        notification_date=timezone.now()
    )
    notification.save()
    return redirect('subscription')


def invite_friend(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        room_id = request.POST.get('room_id')
        receiver = get_object_or_404(CustomUser, id=user_id)
        room = get_object_or_404(Room, id=room_id)

        notification = Notifications(
            sender=request.user,
            receiver=receiver,
            text_notification=f"{request.user.username} отправил(а) вам приглашение в комнату.",
            room_link=room.room_name,
            notification_date=timezone.now()
        )
        notification.save()

        return JsonResponse({'status': 'success', 'message': f'{receiver.username} приглашен в комнату {room.room_name}'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
