from rest_framework import serializers

from instagram.models import AccessToken


class AccessTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessToken
        fields = ['access_token', 'expire']
