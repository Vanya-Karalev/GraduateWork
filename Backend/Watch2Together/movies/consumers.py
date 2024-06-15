import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from movies.models import *
from users.models import *
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if 'pause_state' in text_data_json:
            room_name = text_data_json['room_name']
            new_pause_state = text_data_json['pause_state']
            await self.update_pause_state(room_name, new_pause_state)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'pause_state',
                    'pause_state': new_pause_state,
                }
            )
        elif 'timer_state' in text_data_json:
            room_name = text_data_json['room_name']
            new_timer_state = text_data_json['timer_state']
            await self.update_timer_state(room_name, new_timer_state)
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'timer_state',
                    'timer_state': new_timer_state,
                }
            )
        elif 'connect_user' in text_data_json:
            await self.connect_room_users(text_data_json['room_name'], text_data_json['connect_user'])
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'connect_user',
                    'connect_user': text_data_json['connect_user'],
                }
            )
        elif 'disconnect_user' in text_data_json:
            await self.disconnect_room_users(text_data_json['room_name'], text_data_json['disconnect_user'])
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'disconnect_user',
                    'disconnect_user': text_data_json['disconnect_user'],
                }
            )
        elif 'disconnect' in text_data_json:
            print('стр закрыта')
        else:
            message = text_data_json
            event = {
                'type': 'send_message',
                'message': message,
            }
            await self.channel_layer.group_send(self.room_name, event)

    async def connect_user(self, event):
        user = await sync_to_async(get_object_or_404)(CustomUser, username=event['connect_user'])
        if user.image and hasattr(user.image, 'url'):
            image_url = user.image.url
        else:
            image_url = None
        await self.send(text_data=json.dumps({
            'type': 'connect',
            'connect_user': image_url,
            'div_id': user.id
        }))

    async def disconnect_user(self, event):
        user = await sync_to_async(get_object_or_404)(CustomUser, username=event['disconnect_user'])
        await self.send(text_data=json.dumps({
            'type': 'disconnect',
            'div_id': user.id
        }))

    async def send_message(self, event):
        data = event['message']
        await self.create_message(data=data)
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    async def pause_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'pause_state',
            'pause_state': event['pause_state']
        }))

    async def timer_state(self, event):
        await self.send(text_data=json.dumps({
            'type': 'timer_state',
            'timer_state': event['timer_state']
        }))

    @database_sync_to_async
    def connect_room_users(self, room_name, user_username):
        get_room_by_name = Room.objects.get(room_name=room_name)
        user = get_object_or_404(CustomUser, username=user_username)
        if not RoomUsers.objects.filter(room=get_room_by_name, user=user).exists():
            room_users = RoomUsers(room=get_room_by_name, user=user)
            room_users.save()

    @database_sync_to_async
    def disconnect_room_users(self, room_name, user_username):
        get_room_by_name = Room.objects.get(room_name=room_name)
        user = get_object_or_404(CustomUser, username=user_username)
        room_users = RoomUsers.objects.filter(room=get_room_by_name, user=user).first()
        if room_users:
            room_users.delete()

    @database_sync_to_async
    def create_message(self, data):
        get_room_by_name = Room.objects.get(room_name=data['room_name'])
        if not Message.objects.filter(message=data['message']).exists():
            user = get_object_or_404(CustomUser, username=data['sender'])
            new_message = Message(room=get_room_by_name, sender=user, message=data['message'])
            new_message.save()

    @database_sync_to_async
    def update_pause_state(self, room_name, new_pause_state):
        room = Room.objects.get(room_name=room_name)
        room.pause = new_pause_state
        room.save()

    @database_sync_to_async
    def update_timer_state(self, room_name, new_timer_state):
        room = Room.objects.get(room_name=room_name)
        room.timer = new_timer_state
        room.save()
