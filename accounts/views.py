from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User


class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            student_profile = serializer.save()
            if student_profile:
                token = Token.objects.create(user=student_profile.user)
                json = serializer.data
                json['token'] = token.key
                json.pop('password')
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_username_is_valid(request, username):
    if not check_username_length(username):
        return Response({'result': False,
                         'message': 'El nombre de usuario debe tener al menos 4 carácteres'})
    if not check_username_is_available(username):
        return Response({'result': False,
                         'message': 'El nombre de usuario ya esta ocupado'})

    return Response({'result': True})


def check_username_length(username):
    return len(username) > 3


def check_username_is_available(username):
    return not User.objects.filter(username=username).exists()
