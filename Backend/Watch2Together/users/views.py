from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser, Friends
from movies.models import Film, Favorites
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponseForbidden


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('mainpage')
    template_name = 'register.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('mainpage')
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        return super().form_valid(form)


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
    if request.method == 'POST':
        receiver = get_object_or_404(CustomUser, id=user_id)
        friend_request = Friends(sender=request.user, receiver=receiver, status='request_sent')
        friend_request.save()
        return redirect('friends')


def remove_friend(request, friend_id):
    if request.method == 'POST':
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
    if request.method == 'POST':
        sender = get_object_or_404(CustomUser, id=user_id)

        friend_request = get_object_or_404(Friends, sender=sender, receiver=request.user, status='request_sent')

        friend_request.status = 'friends'
        friend_request.save()

        return redirect('friends')


def decline_request(request, user_id):
    if request.method == 'POST':
        receiver = get_object_or_404(CustomUser, id=user_id)

        friendship = Friends.objects.filter(sender=request.user, receiver=receiver).first()

        if friendship:
            friendship.delete()

        return redirect('friends')


def notifications(request):
    return render(request, 'notification.html')


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
