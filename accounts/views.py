from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
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
