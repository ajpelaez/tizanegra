from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from teaching.models import University, Degree


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.university = University("UGR", "Universidad de Granada", "www.ugr.es")
        self.university.save()
        self.degree = Degree("Grado en Ingeniería Informática", self.university)
        self.create_url = reverse('signup')

        self.data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'university': 'UGR'
        }

    def test_when_user_is_created_then_there_are_2_users_in_the_database(self):
        self.client.post(self.create_url, self.data, format='json')
        self.assertEqual(User.objects.count(), 2, "Debería haber 2 usuarios en la base de datos")

    def test_when_user_is_created_then_201_response_is_received(self):
        response = self.client.post(self.create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "La respuesta debería devolver el código 201")

    def test_when_user_is_created_then_the_token_key_is_received_in_the_response(self):
        response = self.client.post(self.create_url, self.data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)


    # def test_create_user_with_no_username(self):
    #     data = {
    #             'username': '',
    #             'email': 'foobarbaz@example.com',
    #             'password': 'foobar'
    #             }
    #
    #     response = self.client.post(self.create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(len(response.data['username']), 1)
    #
    # def test_create_user_with_preexisting_username(self):
    #     data = {
    #             'username': 'testuser',
    #             'email': 'user@example.com',
    #             'password': 'testuser'
    #             }
    #
    #     response = self.client.post(self.create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(len(response.data['username']), 1)
    #
    # def test_create_user_with_preexisting_email(self):
    #     data = {
    #         'username': 'testuser2',
    #         'email': 'test@example.com',
    #         'password': 'testuser'
    #     }
    #
    #     response = self.client.post(self.create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(len(response.data['email']), 1)
    #
    # def test_create_user_with_invalid_email(self):
    #     data = {
    #         'username': 'foobarbaz',
    #         'email': 'testing',
    #         'passsword': 'foobarbaz'
    #     }
    #
    #     response = self.client.post(self.create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(len(response.data['email']), 1)
    #
    # def test_create_user_with_no_email(self):
    #     data = {
    #         'username': 'foobar',
    #         'email': '',
    #         'password': 'foobarbaz'
    #     }
    #
    #     response = self.client.post(self.create_url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(User.objects.count(), 1)
    #     self.assertEqual(len(response.data['email']), 1)