from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from .models import Binary
from .serializers import BinarySerializer

from django.contrib.auth.models import User

import json


def is_admin_permissions(func):
    def wrapper(self, request):
        if not bool(request.user and request.user.is_staff):
            data = {
                "detail": "You do not have permission to perform this action."
            }
            return Response(data=json.dumps(data), status=status.HTTP_403_FORBIDDEN)
        return func(self, request)
    return wrapper


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = request.data

        try:
            username = data['username']
            password = data['password']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            User.objects.get(username=username)
            try:
                user = User.objects.get(username=username, password=password)
            except:
                data = {
                    "detail": "Invalid password!"
                }
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except:
            user = User.objects.create(username=username, password=password)

        try:
            user_token = user.auth_token.key
        except:
            Token.objects.create(user=user)
            user_token = user.auth_token.key

        data = {'token': user_token}
        return Response(data=data, status=status.HTTP_200_OK)


class BinaryView(APIView):
    def get(self, request):
        binaries = Binary.objects.all()
        serializer = BinarySerializer(binaries, many=True)
        # data_keys = json.dumps({"keys": [i['key'] for i in serializer.data]})
        # return Response({'binary': data_keys})
        return Response({'binary': serializer.data})

    @is_admin_permissions
    def post(self, request):
        binary = request.data.get('binary')
        serializer = BinarySerializer(data=binary)

        if Binary.objects.filter(key=binary['key']):
            return Response({"success": "The key {} is already exist!".format(binary['key'])})

        if serializer.is_valid(raise_exception=True):
            binary_saved = serializer.save()

        return Response({"success": "Binary {} created successfully".format(binary_saved)})

    def patch(self, request):
        binary = request.data.get('binary')
        serializer = BinarySerializer(data=binary)

        if binary == Binary.objects.filter(key=binary['key'])[0]:
            return Response({"success": "No changes "})

        if serializer.is_valid(raise_exception=True):
            binary_saved = serializer.save()

        return Response({"success": "Binary {} changed successfully".format(binary_saved)})

    @is_admin_permissions
    def delete(self, request):
        binary = request.data.get('binary')
        serializer = BinarySerializer(data=binary, partial=True)
        serializer.validate_key(binary)

        if not Binary.objects.filter(key=binary['key']):
            return Response({"success": "No such key!"})

        if serializer.is_valid(raise_exception=True):
            binary_deleted = serializer.delete(serializer.validated_data)

        return Response({"success": "Binary {} deleted successfully".format(binary_deleted)})
