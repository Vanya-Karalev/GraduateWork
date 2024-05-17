from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import authenticate, login, logout
from users.forms import CustomUserCreationForm, CustomUserChangeForm


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
    return render(request, 'friends.html')


def notifications(request):
    return render(request, 'notification.html')


def subscription(request):
    return render(request, 'subscription.html')
