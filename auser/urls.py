# from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path

from auser.views import (
    InviteUserEmailView, UserFirstLoginView, RegisterView, TestView,
    LoginView, UserView, GetOnlineUsersView
)

urlpatterns = [
    path('auth/user/', UserView.as_view(), name='user'),
    path('auth/login/', LoginView.as_view(), name="login"),
    # path('auth/password/reset/confirm/<uidb64>/<token>/',
    #      PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/auth/first-login/', UserFirstLoginView.as_view(), name='user-first-login'),

    path('auth/invite/registration/<uidb64>/<iiboa>/<token>/', RegisterView.as_view(), name='invite-register'),
    path('auth/invite/', InviteUserEmailView.as_view(), name='get-online-users'),
    path('get-online-users/', GetOnlineUsersView.as_view(), name='hello'),
    path('auth/hello/', TestView.as_view(), name='hello'),

]
