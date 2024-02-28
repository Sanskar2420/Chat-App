from django.views import View
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from Users.services import CreateChatGroupService, ListOfUsersService, RegisterUserService


@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        return RegisterUserService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return RegisterUserService(request=request).post_view()
    

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from Users.services import RegisterUserService, LoginService, HomeViewService, CreateRoomService


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HomeViewService(request=request).get_view()


@method_decorator(csrf_exempt, name='dispatch')
class RegisterUser(View):
    def get(self, request, *args, **kwargs):
        return RegisterUserService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return RegisterUserService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class Login(View):
    def get(self, request, *args, **kwargs):
        return LoginService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return LoginService(request=request).post_view()


# @method_decorator(csrf_exempt, name='dispatch')
# class UpdateProfile(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return UpdateProfileService(request=request).get_view()

#     def post(self, request, *args, **kwargs):
#         return UpdateProfileService(request=request).post_view()


# @method_decorator(csrf_exempt, name='dispatch')
# class Followers(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return FollowersService(request=request).get_view()

#     def post(self, request, *args, **kwargs):
#         return FollowersService(request=request).post_view()


@method_decorator(csrf_exempt, name='dispatch')
class ListOfUsers(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return ListOfUsersService(request=request).get_view()

    def post(self, request, *args, **kwargs):
        return ListOfUsersService(request=request).post_view()


# @method_decorator(csrf_exempt, name='dispatch')
# class Following(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return FollowingService(request=request).get_view()

#     def post(self, request, *args, **kwargs):
#         return FollowingService(request=request).post_view()


# class DisplayAnotherUserProfile(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         return DisplayAnotherUserProfileService(request=request, id=kwargs.get("id")).get_view()


@method_decorator(csrf_exempt, name='dispatch')
class CreateChatRoom(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CreateRoomService(request=request).post_view()
    
@method_decorator(csrf_exempt, name="dispatch")
class CreateChatGroup(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CreateChatGroupService(request=request, kwargs=kwargs).post_view()
