import requests
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

TOKEN = "1765593014:AAFx3vHUndFOHwPsaep2b70jyz3rxZ7nQ5c"


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_subscribers_count(request):
    link = request.GET.get('link')
    username = '@' + link.split('/')[len(link.split('/'))-1]
    url = 'https://api.telegram.org/bot'+TOKEN+'/getChatMemberCount'
    count = requests.get(url=url, params={'chat_id': username})
    return Response(count.json())


