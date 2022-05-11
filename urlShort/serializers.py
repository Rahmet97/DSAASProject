from rest_framework import serializers
from .models import UrlShort


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlShort
        fields = ['original_url']
