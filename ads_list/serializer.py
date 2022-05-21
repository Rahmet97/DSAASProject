from rest_framework import serializers

from .models import ADS_list

class ADSSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADS_list
        fields = ['id', 'name', 'ssilka', 'vid', 'sybscribe', 'oxvat', 'cost']