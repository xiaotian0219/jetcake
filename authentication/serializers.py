from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'groups', 'user_permissions')


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        read_only_fields = ('id')
