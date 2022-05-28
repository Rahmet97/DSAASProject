from django.urls import path

from instagram.views import AccessTokenView
from telegram.views import get_chat_subscribers_count

urlpatterns = [
    path('get-chat-subscribers-count/', get_chat_subscribers_count),
    path('access_token/', AccessTokenView.as_view())
]
