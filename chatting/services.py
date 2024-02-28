from django.http import JsonResponse
from django.shortcuts import redirect, render

from chatting.models import Room, Messages
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatRoomService:
    def __init__(self, request, kwargs):
        self.request = request
        self.template_name = 'chatting/room.html'
        self.context = {}
        self.kwargs = kwargs

    def get_view(self):
        room_id=self.kwargs.get('room_id')
        room = Room.objects.filter(room_id=room_id)
        if room:
            room = room.first()
        # sender = self.request.user.id
        # sender_name = User.get_user(filter_kwargs={'id': sender}).username
        # receiver = room.sender.id if room.receiver.id == sender else room.receiver.id
        messages = Messages.objects.filter(room_id=room_id)
        if room.is_group_chat:
            chat_with = room.name
        else:
            participant_ids = set([instance.get("id") for instance in room.participant.values()])
            chat_with_id = list(participant_ids-{self.request.user.id})[0]
            chat_with_object = User.objects.get(id=chat_with_id)
            chat_with = chat_with_object.username
        self.context = {'room_name': room.name, 'sender_id': "sender", 'receiver_id': "receiver",
                    'messages': messages, 'sender_name': "sender_name", 'chat_with':chat_with, "room_id":room.room_id}
        # return redirect('room', kwargs={"room_id":room_id})
        return render(self.request, template_name=self.template_name, context=self.context)
    
    def delete_view(self):
        room_id = self.kwargs.get('room_id')
        room = Room.objects.get(room_id=room_id)
        room.participant.remove(self.request.user)
        return redirect('room_list')
    

class ChatRoomListingService:
    def __init__(self, request, *args, **kwargs):
        self.template_name = 'chatting/room_list.html'
        self.context = {}
        self.kwargs = kwargs
        self.request = request

    def get_view(self):
        user = self.request.user
        rooms = Room.objects.filter(participant=user)
        self.context = {"rooms":rooms}
        return render(self.request, template_name=self.template_name, context=self.context)


class DeleteMessageService:
    def __init__(self, request, kwargs) -> None:
        self.request = request
        self.kwargs = kwargs

    def get_view(self):
        id = self.kwargs.get("id")
        message = Messages.objects.filter(id=id).update(is_deleted=True)
        if message:
            return JsonResponse({"msg":"SUCCESS"})
        return JsonResponse({"msg":"SOMETHING WENT WRONG"})