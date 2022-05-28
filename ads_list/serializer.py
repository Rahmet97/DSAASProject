from rest_framework import serializers

from .models import ADS_list


class ADSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADS_list
        fields = '__all__'
