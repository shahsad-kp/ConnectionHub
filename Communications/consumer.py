import json
from typing import Optional

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user: Optional['User'] = None
        self.chat_room = None

    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_room = f'user_chatroom_{self.user.id}'

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        received_data = json.loads(event['text'])
        message_text = received_data.get('message')
        username = received_data.get('username')

        other_user = await self.get_user_object(username)
        if not other_user:
            return False
        other_user_chat_room = f'user_chatroom_{other_user.id}'

        if not message_text:
            return False

        message = await self.create_chat_message(message_text, other_user)

        response = {
            'message': message.message,
            'sender': {
                'username': message.sender.username,
                'fullname': message.sender.full_name or message.sender.username,
                'avatar': message.sender.profile_picture.url,
                'id': message.sender.id
            },
            'receiver': {
                'username': message.receiver.username,
                'fullname': message.receiver.full_name or message.receiver.username,
                'avatar': message.receiver.profile_picture.url,
                'id': message.receiver.id
            },
            'timestamp': message.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        }

        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    async def chat_message(self, event):
        response = json.loads(event['text'])
        if response['sender']['id'] == self.user.id:
            response['is_sender'] = True
        else:
            response['is_sender'] = False

        await self.send({
            'type': 'websocket.send',
            'text': json.dumps(response)
        })

    @database_sync_to_async
    def get_user_object(self, username: str):
        from Users.models import User
        qs = User.objects.filter(username=username)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, message: str, other_user: 'Users.User'):
        from .models import Message
        obj = Message.objects.create(
            message=message,
            sender=self.user,
            receiver=other_user
        )
        return obj
