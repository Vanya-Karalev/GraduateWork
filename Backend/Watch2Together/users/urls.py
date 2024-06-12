from django.urls import path
from users.views import SignUpView, ProfileView
from . import views


urlpatterns = [
    path('buy-subscription/<int:days>', views.buy_subscription, name='buy_subscription'),
    path('cancel-subscription/', views.cancel_subscription, name='cancel_subscription'),
    path('myfavoritefilms/', views.my_favorite_films, name='myfavoritefilms'),
    path('favorite/<int:film_id>', views.favorite, name='favorite'),
    path('friends/', views.friends, name='friends'),
    path('friends/<int:user_id>', views.add_friend, name='add_friend'),
    path('remove_friend/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('accept_request/<int:user_id>/', views.accept_request, name='accept_request'),
    path('decline_request/<int:user_id>/', views.decline_request, name='decline_request'),
    path('notifications/', views.notifications, name='notifications'),
    path('subscription/', views.subscription, name='subscription'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('signin/', views.LoginPage, name="signin"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutPage, name='logout'),
]