import html
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from core.models import Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get room name from url and create a room group
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # read recieved message and user ids
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = text_data_json["sender"]
        receiver_id = text_data_json["receiver"]

        # get users and create message object in database
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)
        await sync_to_async(Message.objects.create)(
            sender=sender, receiver=receiver, message=message
        )

        message = html.escape(message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "sender": sender},
        )

    async def chat_message(self, event):
        # Get parameters from event
        message = event["message"]
        sender = event["sender"]

        data = {
            "message": message,
            "sender_id": str(sender.id),
            "sender_image": sender.profile_photo.url,
        }

        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))
