from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import AccessTokenSerializer

import os
from datetime import datetime

import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from dotenv import load_dotenv

from .models import AccessToken

load_dotenv()


class AccessTokenView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AccessTokenSerializer

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MainData(APIView):
    permission_classes = (IsAuthenticated,)
    base_url = 'https://graph.facebook.com/v15.0/'

    def getPageID(self, user_id, access_token):
        response = requests.get(f'{self.base_url}me/accounts', params={
            'access_token': access_token
        })
        return response.json()

    def getInstagramBusinessID(self, user_id, access_token):
        page_data = self.getPageID(user_id, access_token)
        page_id = page_data['data'][0]['id']
        response = requests.get(f'{self.base_url}{page_id}', params={
            'fields': 'instagram_business_account',
            'access_token': access_token
        })
        return response.json()

    def check_token(self, access):
        response = requests.get('https://graph.facebook.com/debug_token', params={
            'input_token': access,
            'access_token': access
        })

        print(response.json())
        return response.json()

    def refresh(self, access):
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')

        response = requests.get(f'{self.base_url}oauth/access_token', params={
            'grant_type': 'fb_exchange_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'fb_exchange_token': access
        })
        return response.json()

    def get(self, request):
        access_token = AccessToken.objects.get(user=request.user)

        if access_token.expire < int(round(datetime.now().timestamp())):
            new_token = self.refresh(access_token.access_token)
            expire = self.check_token(new_token['access_token'])['data']['data_access_expires_at']
            access_token.access_token = new_token['access_token']
            access_token.expire = expire
            access_token.save()
        business_account_data = self.getInstagramBusinessID(request.user.id, access_token.access_token)
        insta_business_id = business_account_data['instagram_business_account']['id']
        main_data = requests.get(f'{self.base_url}{insta_business_id}', params={
            'fields': 'media_count,followers_count,follows_count,ig_id',
            'access_token': access_token.access_token
        })
        insights = requests.get(f'{self.base_url}{insta_business_id}/insights', params={
            'metric': 'audience_city,audience_country,audience_gender_age',
            'period': 'lifetime',
            'access_token': access_token.access_token
        })
        return Response({
            "main_data": main_data.json(),
            "insights": insights.json()
        })
