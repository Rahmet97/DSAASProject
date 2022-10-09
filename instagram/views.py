import requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import AccessToken
from .serializers import AccessTokenSerializer


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_followers(request):
    link = request.GET.get('link')
    username = '@' + link.split('/')[len(link.split('/'))-1]
    url = ''
    count = requests.get(url=url, params={'chat_id': username})
    return Response(count.json())


class AccessTokenView(CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AccessTokenSerializer

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = AccessToken.objects.create(access_token=serializer.data["access_token"],
                                                  expire=serializer.data["expire"],
                                                  user=request.user)
        access_token.save()
        data = {
            "success": True,
            "message": "Successfully"
        }
        return Response(data)
