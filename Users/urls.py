from django.urls import path
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from Users.views import CreateChatGroup, ListOfUsers, Login, RegisterUser, CreateChatRoom

urlpatterns = [
    path('register-user/', RegisterUser.as_view(), name='register'),
    path('', Login.as_view(), name='login'),
    path('list-users/', ListOfUsers.as_view(), name='list-users'),
    path('chat-create/', CreateChatRoom.as_view(), name='chat_create'),
    path('group-create/',CreateChatGroup.as_view(), name="group_create"),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name='Users/password_reset.html',
             html_email_template_name='Users/password_reset_email.html'
         ),
         name='password-reset'
         ),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='Users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='Users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='Users/password_reset_complete.html'),
         name='password_reset_complete'),
]
