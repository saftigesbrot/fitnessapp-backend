from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client.force_authenticate(user=self.user)

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword',
            'email': 'new@example.com'
        }
        response = self.client.post('/api/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user(self):
        # Valid ID
        response = self.client.get(f'/user-get?id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['id'], self.user.id)

        # Invalid ID
        response = self.client.get('/user-get?id=9999')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Missing ID
        response = self.client.get('/user-get')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_unauthorized(self):
        self.client.logout() # Ensure unauthenticated (force_authenticate overrides this usually so need to be careful)
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/user-get?id={self.user.id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
