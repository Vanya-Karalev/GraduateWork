from django.urls import path
from . import views


urlpatterns = [
    path('films/', views.get_films, name="films"),
    path('films/<slug:slug>', views.get_film_info, name="film_info"),
    path('', views.get_mainpage, name="mainpage"),
]