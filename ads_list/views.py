from django.shortcuts import render

from ads_list.serializer import ADSSerializer
from rest_framework.permissions import BasePermission, IsAuthenticated
from ads_list.models import ADS_list
from rest_framework import viewsets, generics, response, status
from rest_framework_simplejwt import exceptions, authentication, tokens


class ADS_listView(viewsets.ModelViewSet):
    queryset = ADS_list.objects.all()
    serializer_class = ADSSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_from=self.request.user)
