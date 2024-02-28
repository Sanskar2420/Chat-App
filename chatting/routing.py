from django.urls import path
from chatting import consumers

websocket_urlpatterns = [
    path(r"ws/chat/<str:room_id>/", consumers.ChatConsumer.as_asgi()),
]