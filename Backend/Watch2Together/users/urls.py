from django.urls import path
from users.views import SignUpView, ProfileView
from . import views


urlpatterns = [
    path('friends/', views.friends, name='friends'),
    path('notifications/', views.notifications, name='notifications'),
    path('subscription/', views.subscription, name='subscription'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signin/', views.LoginPage, name="signin"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutPage, name='logout'),
]