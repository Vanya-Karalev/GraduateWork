from django.urls import path
from . import views


urlpatterns = [
    path('films/', views.get_films, name="films"),
    path('', views.get_mainpage, name="mainpage"),
]