from django.shortcuts import render

from rest_framework import status, generics
from rest_framework.response import Response

from rest_framework_jwt.utils import (
    jwt_payload_handler, jwt_encode_handler,
)

from .serializers import UserCreateSerializer


class RegisterView(generics.CreateAPIView):
    authentication_class = ()
    permission_class = ()
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        headers = self.get_success_headers(serializer.data)
        payload = jwt_payload_handler(user)

        response_data = {
            'token': jwt_encode_handler(payload),
            'user': serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
