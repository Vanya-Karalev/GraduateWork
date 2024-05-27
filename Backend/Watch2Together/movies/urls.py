from django.urls import path
from . import views


urlpatterns = [
    path('w2g/<int:film_id>/', views.CreateRoom, name='create-room'),
    path('w2g/<str:room_name>/', views.MessageView, name='room'),
    path('films/', views.get_films, name="films"),
    path('films/<slug:slug>', views.get_film_info, name="film_info"),
    path('films/<slug:slug>/watch', views.watch_film, name="watch_film"),
    path('', views.get_mainpage, name="mainpage"),
]