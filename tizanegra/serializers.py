from rest_framework import serializers
from django.contrib.auth.models import User
from .models import University, Degree, Student


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    password = serializers.CharField(source='user.password')
    university = serializers.CharField()
    degree = serializers.CharField()

    def create(self, validated_data):
        university = University.objects.get(acronym=validated_data['university'])
        degree = Degree.objects.get(acronym=validated_data['degree'], university=university)
        user = User.objects.create_user(validated_data['user']['username'],
                                        validated_data['user']['email'] + university.email_extension,
                                        validated_data['user']['password'])

        student = Student.objects.create(user=user, university=university, degree=degree)
        return student

    class Meta:
        model = Student
        fields = ('id', 'username', 'email', 'password', 'university', 'degree')
