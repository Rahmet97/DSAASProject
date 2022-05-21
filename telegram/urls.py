from django.urls import path

from telegram.views import get_chat_subscribers_count, add_channel_or_group, add_post

urlpatterns = [
    path('get-chat-subscribers-count', get_chat_subscribers_count),
    path('add-channel-or-group', add_channel_or_group),
    path('add-post', add_post)
]
