from django.urls import path
from chatting.views import ChatRoom, ChatRoomDelete, ChatRoomListingView, DeleteMessageView

urlpatterns = [
    path("room-lists/", ChatRoomListingView.as_view(), name="room_list"),
    path("<str:room_id>/", ChatRoom.as_view(), name="room"),
    path("delete/<str:room_id>", ChatRoomDelete.as_view(), name="delete-chat"),
    path("delete-message/<int:id>", DeleteMessageView.as_view(), name='delete_message'),
]
