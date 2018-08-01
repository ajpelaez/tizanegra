from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render
import re


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
    if len(username) < 4:
        return Response({'result': False,
                         'message': 'El nombre de usuario debe tener al menos 4 carácteres'})

    if re.match("^[a-zA-Z0-9_.-]+$", username) is None:
        return Response({'result': False,
                         'message': 'El nombre de usuario no puede incluir alguno de los símbolos utilizados'})

    if User.objects.filter(username=username).exists():
        return Response({'result': False,
                         'message': 'Este nombre de usuario ya esta siendo usado'})

    return Response({'result': True})


@api_view(['GET'])
def check_email_is_valid(request, email):
    if User.objects.filter(email=email).exists():
        return Response({'result': False,
                         'message': 'El email introducido ya esta siendo usado'})
    return Response({'result': True})


class UserPanelView(View):

    def get(self, request):
        context = {'test': 'hi'}
        return render(request, 'registration/panel.html', context)
