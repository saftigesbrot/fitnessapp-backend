from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ScoringCurrent, ScoringTop, ScoringAllTime, LevelCurrent

class ScoringTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        ScoringCurrent.objects.create(user=self.user, value=100)
        ScoringTop.objects.create(user=self.user, value=200)
        LevelCurrent.objects.create(user=self.user, level=5, xp=500)

    def test_get_current_scoring(self):
        response = self.client.get('/scoring-get?type=current')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 100)

    def test_get_top_scoring(self):
        response = self.client.get('/scoring-get?type=top')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['value'], 200)

    def test_get_level(self):
        response = self.client.get('/scoring-level')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['level'], 5)
        self.assertEqual(response.data['xp'], 500)
