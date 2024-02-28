# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chatting.models import Messages, Room
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def save_message(self, message_data):
        return Messages.objects.create(**message_data)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]
        room = text_data_json["room"]
        room_object = Room.objects.filter(room_id=room).first()
        time_message = self.save_message(message_data={'sender_id': int(sender), 'message': message, "room":room_object})
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, 'sender': sender ,'time': time_message.timestamp.strftime("%m/%d/%Y, %H:%M:%S"), "sender_name":time_message.sender.username}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        time = event['time']
        sender_name = event["sender_name"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message, 'sender': sender, 'time_final': time, "sender_name":sender_name}))
