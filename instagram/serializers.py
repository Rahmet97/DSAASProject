from rest_framework import serializers

from instagram.models import AccessToken


class AccessTokenSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return AccessToken.objects.create(**validated_data)

    class Meta:
        model = AccessToken
        fields = ['user', 'access_token', 'expire']
