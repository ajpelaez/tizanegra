from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from accounts.models import StudentProfile
from teaching.models import University


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    university = serializers.CharField()

    def create(self, validated_data):
        university = University.objects.get(acronym=validated_data['university'])
        user = User.objects.create_user(validated_data['user']['username'], validated_data['user']['email'],
                                        validated_data['user']['password'])

        student_profile = StudentProfile.objects.get(user=user)
        student_profile.university = university
        return student_profile

    class Meta:
        model = StudentProfile
        fields = ('id', 'username', 'email', 'password', 'university')
