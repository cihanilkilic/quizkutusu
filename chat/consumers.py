import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.recipient = self.scope['url_route']['kwargs']['recipient']
        self.user = self.scope['user']

        if self.user.is_authenticated:
            # İki kullanıcının özel bir gruba katılmasını sağla
            self.room_group_name = f"chat_{min(self.user.username, self.recipient)}_{max(self.user.username, self.recipient)}"

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        recipient = text_data_json['recipient']
        sender = text_data_json['sender']

        # Save message to database
        await sync_to_async(self.save_message)(sender, recipient, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender
            }
        )

    def save_message(self, sender, recipient, message):
        sender_user = User.objects.get(username=sender)
        recipient_user = User.objects.get(username=recipient)
        Message.objects.create(sender=sender_user, recipient=recipient_user, message=message)

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))
