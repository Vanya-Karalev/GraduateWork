from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/notification/<uuid:room_name>/', ChatConsumer.as_asgi()),
]