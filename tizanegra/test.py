from django.urls import reverse

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import University, Degree


class AccountsTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.university = University(acronym="UGR", name="Universidad de Granada", web="www.ugr.es",
                                     email_extension="@correo.ugr.es")
        self.university.save()
        self.degree = Degree(acronym="GII", name="Grado en Ingeniería Informática", university=self.university)
        self.degree.save()

        self.example_signup_data = {
            'username': 'foobar',
            'email': 'foobar',
            'password': 'somepassword',
            'university': 'UGR',
            'degree': 'GII'
        }

    def test_when_user_is_created_then_there_are_2_users_in_the_database(self):
        self.url = reverse('signup')
        self.client.post(self.url, self.example_signup_data, format='json')
        self.assertEqual(User.objects.count(), 2, "Debería haber 2 usuarios en la base de datos")

    def test_when_user_is_created_then_201_response_is_received(self):
        self.url = reverse('signup')
        response = self.client.post(self.url, self.example_signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, "La respuesta debería devolver el código 200")

    def test_when_username_is_already_taken_then_username_is_not_valid(self):
        url = reverse('check_username', kwargs={'username': 'testuser'})

        response = self.client.get(url, format='json')
        self.assertFalse(response.data['result'],
                         "El resultado de la respuesta debería ser falso, ya que usuario no es válido")

    def test_when_username_is_smaller_than_4_characters_then_username_is_not_valid(self):
        url = reverse('check_username', kwargs={'username': 'tes'})

        response = self.client.get(url, format='json')
        self.assertFalse(response.data['result'],
                         "El resultado de la respuesta debería ser falso, ya que usuario no es válido")

    def test_when_email_is_already_taken_then_email_is_invalid(self):
        url = reverse('check_email', kwargs={'email': 'test@example.com'})

        response = self.client.get(url, format='json')
        self.assertFalse(response.data['result'],
                         "El resultado de la respuesta debería ser falso, ya que email no es válido")
