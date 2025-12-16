from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterTests(APITestCase):
    def test_register_user(self):
        url = reverse('auth_register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_missing_password(self):
        url = reverse('auth_register')
        data = {
            'username': 'testuser_nopass',
            'email': 'nopass@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        # Create first users
        User.objects.create_user(username='testuser', email='test1@example.com', password='password')
        
        url = reverse('auth_register')
        data = {
            'username': 'testuser',
            'password': 'newpassword123',
            'email': 'test2@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_duplicate_email(self):
        # Create first users
        User.objects.create_user(username='testuser1', email='test@example.com', password='password')
        
        url = reverse('auth_register')
        data = {
            'username': 'testuser2',
            'password': 'newpassword123',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_missing_email(self):
        url = reverse('auth_register')
        data = {
            'username': 'noemailuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
