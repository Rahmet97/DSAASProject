from django.shortcuts import render
from requests import Response

from ads_list.serializer import ADSSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from ads_list.models import ADS_list
from rest_framework import viewsets, generics, response, status
from rest_framework_simplejwt import exceptions, authentication, tokens


from rest_framework.views import APIView
from django.http import Http404


class ADSView(generics.ListCreateAPIView):
    queryset = ADS_list.objects.all()
    serializer_class = ADSSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]
    

class ADSDestroyAPIView(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ADS_list.objects.get(pk=pk)
        except ADS_list.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        ads = self.get_object(pk)
        ads.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
