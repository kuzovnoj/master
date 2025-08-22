from rest_framework import serializers
from .models import ZakazNaryad

class ZakazNaryadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZakazNaryad
        fields = ['auto', 'client', 'master', 'remont', 'price']