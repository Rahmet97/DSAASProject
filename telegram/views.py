import datetime

import requests
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.conf import settings
from .models import Post, TGChannel


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_subscribers_count(request):
    link = request.GET.get('link')
    username = '@' + link.split('/')[len(link.split('/'))-1]
    url = 'https://api.telegram.org/bot'+settings.BOT_TOKEN+'/getChatMemberCount'
    count = requests.get(url=url, params={'chat_id': username})
    return Response(count.json())


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_channel_or_group(request):
    try:
        if TGChannel.objects.filter(user_id=request.user.id).exists():
            data = {
                "success": False,
                "error": "Telegram kanal yoki gruppa kiritilgan."
            }
        else:
            link = request.POST.get("link", "")
            current_user = request.user
            post = TGChannel.objects.create(link=link, user_id=current_user.id)
            post.save()
            data = {
                "success": True,
                "message": "Kanal yoki gruppa qo'shildi"
            }
    except Exception as e:
        data = {
            "success": False,
            "error": f'{e}'
        }
    return Response(data)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_post(request):
    try:
        date = request.POST.get("date", "")
        link = request.POST.get("link", "")
        link_name = request.POST.get("link_name", "")
        description = request.POST.get("description", "")
        hashtag = request.POST.get("hashtag", "")
        file = request.POST.get("file", "")
        current_user = request.user

        post = Post.objects.create(date=date, link=link, link_name=link_name, description=description, hashtag=hashtag, file=file, user_id=current_user.id)
        post.save()
        data = {
            "success": True,
            "message": "Post qo'shildi"
        }
    except Exception as e:
        data = {
            "success": False,
            "error": f'{e}'
        }
    return Response(data)
