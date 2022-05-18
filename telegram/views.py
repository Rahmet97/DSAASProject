import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .tasks import auto_post

TOKEN = "5269482912:AAHYYrQ5nR_yrKp9ay8PAfulTatXSuGCh6A"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_subscribers_count(request):
    link = request.GET.get('link')
    username = '@' + link.split('/')[len(link.split('/'))-1]
    url = 'https://api.telegram.org/bot'+TOKEN+'/getChatMemberCount'
    count = requests.get(url=url, params={'chat_id': username})
    return Response(count.json())


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def auto_posting(request):
    auto_post.delay()
    return Response({"success": True})
