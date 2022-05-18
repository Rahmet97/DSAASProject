from django.urls import path

from telegram.views import get_chat_subscribers_count

urlpatterns = [
    path('get-chat-subscribers-count', get_chat_subscribers_count)
]
