from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_password(self, value: str) -> str:
        return make_password(value)