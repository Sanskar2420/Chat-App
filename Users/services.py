import json
import re
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.contrib import messages
# from Users.tasks import print_func
from Users.constants import ACCOUNT_DISABLED, EMAIL_PATTERN, FIELDS_MISSING, INVALID_CREDENTIALS, INVALID_EMAIL_FORMAT, INVALID_PASSWORD_FORMAT, INVALID_USERNAME_FORMAT, LIST_OF_USER_TEMPLATE, LOGIN_TEMPLATE, PASSWORD_PATTERN, REGISTER_TEMPLATE, SOMETHING_WENT_WRONG, USER_CREATED, USER_EXISTS, USERNAME_PATTERN
from chatting.models import Room


User = get_user_model()

class RegisterUserService:
    def __init__(self, request):
        self.request = request
        self.template = REGISTER_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            print(f"Error : {err}")
            return redirect('login')

    def post_view(self):
        """
        Register a user by providing First Name, Last Name, Email, Username, Password, Superuser checkbox
        """
        try:
            self.context = {
                'user': User.objects.filter(username=self.request.user.username)
            }

            firstname = self.request.POST.get('first').strip()
            lastname = self.request.POST.get('last').strip()
            email = self.request.POST.get('email').replace(" ", "")
            username = self.request.POST.get('username').replace(" ", "")
            password = self.request.POST.get('password').replace(" ", "")

            # check if username matches validation
            username_pattern = USERNAME_PATTERN
            if not re.match(username_pattern, username):
                self.context['error'] = INVALID_USERNAME_FORMAT
                return render(self.request, template_name=self.template, context=self.context)
            # check if password matches validation
            password_pattern = PASSWORD_PATTERN
            if not re.match(password_pattern, password):
                self.context['error'] = INVALID_PASSWORD_FORMAT
                return render(self.request, template_name=self.template, context=self.context)
            # check if email matches validation
            email_pattern = EMAIL_PATTERN
            if not re.match(email_pattern, email):
                self.context['error'] = INVALID_EMAIL_FORMAT
                return render(self.request, template_name=self.template, context=self.context)

            # Check if all the required data is available or not
            if firstname and lastname and email and username and password:
                user_email = User.objects.filter(email=email)
                # If user with given email id not exist
                if not user_email:
                    user_name = User.objects.filter(username=username)
                    # If user with given username not exist
                    if not user_name:
                        # Prepare data to create new user
                        user_data = {'first_name': firstname, 'last_name': lastname, 'username': username,
                                     'email': email, 'password': password}
                        # Create new user
                        msg = self.__save_new_user(user_details=user_data)
                        # messages.success(self.request, msg)

                        # redirect user on Register new user page.
                        return redirect('login')
                    else:
                        # If user with given username exist show the error using messages
                        msg = USER_EXISTS.format(user_name.username)
                        self.context['error'] = msg
                        return render(self.request, template_name=self.template, context=self.context)
                else:
                    # If user with given user email exist show the error using messages
                    msg = USER_EXISTS.format(user_email.email)
                    self.context['error'] = msg
                    return render(self.request, template_name=self.template, context=self.context)
            else:
                msg = FIELDS_MISSING
                self.context['error'] = msg
                return render(self.request, template_name=self.template, context=self.context)
        except Exception as error:
            self.context['error'] = SOMETHING_WENT_WRONG
            return render(self.request, template_name=self.template, context=self.context)

    def __save_new_user(self, user_details):
        """
        Get the raw password and save it as new password.
        If details are valid and user gets created with user details, an email will be sent to the registered email address with
            username, raw password and link to change password
        @param user_details: User details like username, password, etc.
        """
        # Create copy of plain temporary password to send in email.
        plain_password = user_details.get('password')
        # Encrypts plain password/Creates a hash of password for security purpose.
        user_details['password'] = make_password(password=plain_password)
        obj = User.objects.create(**user_details)
        return USER_CREATED.format(obj.username)
    

class HomeViewService:
    def __init__(self, request):
        self.request = request

    def get_view(self):
        return redirect('login')



class LoginService:
    def __init__(self, request):
        self.request = request
        self.template = LOGIN_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            print(f"Error : {err}")
            return redirect('login')

    def post_view(self):
        """
        Take username and password from user.
        @return: redirect home if user is authenticated, 2fa if its enabled, error if no user found.
        """
        try:
            username = self.request.POST.get("username").replace(" ", "")
            password = self.request.POST.get("password").replace(" ", "")
            # if self.request.user.is_authenticated:
            #     return redirect('show-question')    
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                if not user.is_active:
                    self.context['error'] = ACCOUNT_DISABLED
                    return render(self.request, template_name=self.template, context=self.context)
                login(self.request, user)
                # print_func.delay(user=user.email)
                next_page = self.request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect('list-users')
            else:
                self.context['error'] = INVALID_CREDENTIALS
                return render(self.request, template_name=self.template, context=self.context)
        except Exception as err:
            self.context['error'] = SOMETHING_WENT_WRONG
            return render(self.request, template_name=self.template, context=self.context)


# class UpdateProfileService:
#     def __init__(self, request):
#         self.request = request
#         self.template_name = PROFILE_TEMPLATE
#         self.context = {}

#     def get_view(self):
#         try:
#             self.context['user'] = User.get_user(filter_kwargs={"id": self.request.user.id})
#             return render(self.request, template_name=self.template_name, context=self.context)
#         except Exception as err:
#             print(f"Error : {err}")
#             return redirect('show-question')

#     def post_view(self):
#         try:
#             data = json.loads(json.dumps(self.request.POST))
#             user = User.get_user(filter_kwargs={"id": self.request.user.id})
#             if data.get('password') and data.get('password') == data.get('re_type_password'):
#                 User.set_new_password(user=user, password=data.get('password'))
#             User.update_user(filter_kwargs={"id": self.request.user.id},
#                              update_kwargs={"first_name": data.get("firstname"), "last_name": data.get("lastname")})
#             return redirect('profile')
#         except Exception as err:
#             self.context['user'] = User.get_user(filter_kwargs={"id": self.request.user.id})
#             return render(self.request, template_name=self.template_name, context=self.context)


# class FollowersService:

#     def __init__(self, request):
#         self.request = request
#         self.template_name = FOLLOWERS_TEMPLATE
#         self.context = {}

#     def get_view(self):
#         try:
#             self.context['pending_users'] = FollowTable.get_users(
#                 filter_kwargs={"request_to": self.request.user.id, "status": "PENDING"})
#             self.context['accepted_users'] = FollowTable.get_users(
#                 filter_kwargs={"request_to": self.request.user.id, "status": "ACCEPTED"})
#             return render(self.request, template_name=self.template_name, context=self.context)
#         except Exception as err:
#             return redirect('show-question')

#     def post_view(self):
#         try:
#             data = json.loads(self.request.body)
#             FollowTable.update_record(
#                 filter_kwargs={"request_to": data.get("request_user"), "request_by": data.get("user_id")},
#                 update_kwargs={"status": "ACCEPTED" if bool(data.get("value")) else "REJECTED"})
#             return JsonResponse({"msg": "Success"})
#         except Exception as err:
#             return JsonResponse({"msg": SOMETHING_WENT_WRONG})


# class FollowingService:
#     def __init__(self, request):
#         self.request = request
#         self.template_name = FOLLOWING_TEMPLATE
#         self.context = {}

#     def get_view(self):
#         try:
#             self.context['pending_users'] = FollowTable.get_users(
#                 filter_kwargs={"request_by": self.request.user.id, "status": "PENDING"})
#             self.context['accepted_users'] = FollowTable.get_users(
#                 filter_kwargs={"request_by": self.request.user.id, "status": "ACCEPTED"})
#             return render(self.request, template_name=self.template_name, context=self.context)
#         except Exception as err:
#             return redirect('show-question')

#     def post_view(self):
#         try:
#             data = self.request.POST
#             FollowTable.update_record(
#                 filter_kwargs={"request_to": data.get("user_id"), "request_by": self.request.user},
#                 update_kwargs={"status": "REJECTED"})
#             return JsonResponse({"msg": "Success"})
#         except Exception as err:
#             return JsonResponse({"msg": SOMETHING_WENT_WRONG})


class ListOfUsersService:
    def __init__(self, request):
        self.request = request
        self.template_name = LIST_OF_USER_TEMPLATE
        self.context = {}

    def get_view(self):
        try:
            self.context['users'] = User.objects.exclude(id=self.request.user.id)
            return render(self.request, template_name=self.template_name, context=self.context)
        except Exception as err:
            breakpoint()
            return redirect('login')


# class DisplayAnotherUserProfileService:
#     def __init__(self, request, id):
#         self.request = request
#         self.template_name = DISPLAY_PROFILE_ONLY_TEMPLATE
#         self.context = {}
#         self.id = id

#     def get_view(self):
#         self.context['user'] = User.get_user(filter_kwargs={"id": self.id})
#         self.context['followers'] = FollowTable.get_users(
#             filter_kwargs={"request_to": self.request.user, "status": "ACCEPTED"})
#         self.context['following'] = FollowTable.get_users(
#             filter_kwargs={"request_by": self.request.user, "status": "ACCEPTED"})
#         self.context['questions'] = Questions.get_all_questions(kwargs={"user": self.request.user})
#         self.context['answers'] = Answers.get_all_answers(kwargs={"user": self.request.user})
#         return render(self.request, template_name=self.template_name, context=self.context)


class CreateRoomService:
    def __init__(self, request):
        self.request = request

    def post_view(self):
        sender = self.request.user.id
        participants = self.request.POST.get('participants')
        is_group = self.request.POST.get("is_group", False)
        # self.request.session['receiver_user'] = receiver
        room = Room.objects.filter(participant=participants).filter(participant=sender)
        if room:
            # print("herherbehrehrgerg cbndfvbuearhbfg")
            new_created_room = room[0]
        else:
            # new_room = get_random_string(10)
            # while True:
            #     room_exists = Room.get_room(kwargs={"name": new_room})
            #     if room_exists:
            #         new_room = get_random_string(10)
            #     else:
            #         break
            new_created_room = Room.objects.create(**{"is_group_chat":is_group})
            participants = User.objects.filter(id__in=participants)
            new_created_room.participant.add(*participants)
            new_created_room.participant.add(self.request.user)
            room_name = new_created_room.name
        return redirect('room', room_id=new_created_room.room_id)



class CreateChatGroupService:
    def __init__(self, request, kwargs):
        self.request = request
        self.kwargs = kwargs

    def post_view(self):
        data = self.request.POST
        group_name = data.get("group_name")
        group_participant_ids = data.get("group_participants").split(',')
        group_participant_ids = [int(i) for i in group_participant_ids if i.isnumeric()]
        group_participants = User.objects.filter(id__in=group_participant_ids)
        new_created_room = Room.objects.create(**{"is_group_chat":True, "name":group_name})
        new_created_room.participant.add(*group_participants)
        new_created_room.participant.add(self.request.user)
        return redirect('room', room_id=new_created_room.room_id)
