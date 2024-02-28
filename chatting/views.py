# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin

# chat/views.py
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests import delete

from chatting.services import ChatRoomListingService, ChatRoomService, DeleteMessageService


@method_decorator(csrf_exempt, name='dispatch')
class ChatRoom(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return ChatRoomService(request=request, kwargs=kwargs).get_view()
    
@method_decorator(csrf_exempt, name='dispatch')
class ChatRoomDelete(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return ChatRoomService(request=request, kwargs=kwargs).delete_view()

class ChatRoomListingView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return ChatRoomListingService(request=request, kwargs=kwargs).get_view()
    
@method_decorator(csrf_exempt, name='dispatch')    
class DeleteMessageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return DeleteMessageService(request=request, kwargs=kwargs).get_view()

    # def post(self, request, *args, **kwargs):
    #     breakpoint()
    #     return DeleteMessageService(request=request, kwargs=kwargs).post_view()