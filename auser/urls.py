from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path, include

from auser.views import (
    InviteUserEmailView, UserFirstLoginView, RegisterView, TestView
)

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),

    path('auth/password/reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/first-login/', UserFirstLoginView.as_view(), name='user-first-login'),

    path('invite/registration/<uidb64>/<iiboa>/<token>/', RegisterView.as_view(), name='invite-register'),
    path('invite/', InviteUserEmailView.as_view(), name='invite_user_email'),
    path('hello/', TestView.as_view(), name='hello'),

]
