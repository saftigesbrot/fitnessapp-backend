from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Scoring, LevelCurrent

class ScoringTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        from django.utils import timezone
        import datetime
        
        # Create a "Top" score (older)
        s1 = Scoring.objects.create(user=self.user, value=200)
        s1.created_at = timezone.now() - datetime.timedelta(days=400)
        s1.save()
        
        # Create a "Current" score (newer, lower value)
        Scoring.objects.create(user=self.user, value=100)
        
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

    def test_leaderboard_filtering(self):
        # Create scores with different dates
        from django.utils import timezone
        import datetime
        now = timezone.now()
        
        # Today's score
        s_today = Scoring.objects.create(user=self.user, value=10)
        
        # Last week score
        s_last_week = Scoring.objects.create(user=self.user, value=20)
        s_last_week.created_at = now - datetime.timedelta(days=10)
        s_last_week.save()

        # Last month score (but within same month if early enough? Let's force prev month)
        # Actually user said "Monthly = Current Month". So let's test "Current Month" logic.
        # If today is 5th, day=30 will be prev month? No, subtract days.
        # Let's just rely on logic: Monthly = This Calendar Month.
        # So a score from last year shouldn't show.
        s_last_year = Scoring.objects.create(user=self.user, value=30)
        s_last_year.created_at = now - datetime.timedelta(days=400)
        s_last_year.save()

        # Test Daily (should only see s_today + setUp score if created today)
        # In setUp: ScoringCurrent created value=100. It defaults to auto_now_add=True (now).
        # So s_today(10) and setup(100) are today. Max is 100.
        res_daily = self.client.get('/scoring-get?type=leaderboard&time_frame=daily')
        self.assertEqual(len(res_daily.data), 1) 
        self.assertEqual(res_daily.data[0]['value'], 100) # Max of today

        # Test Monthly (should see today + setup. Last week (10 days ago) might be same month or not depending on day)
        # Safer check: Last Year should definitely NOT be there.
        res_monthly = self.client.get('/scoring-get?type=leaderboard&time_frame=monthly')
        # Should contain at least today's stuff.
        # Check if s_last_year is present
        values = [x['value'] for x in res_monthly.data]
        self.assertNotIn(30, values) # 30 was last year

    def test_levels_leaderboard(self):
        res = self.client.get('/scoring-get?type=levels')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) > 0)
        self.assertEqual(res.data[0]['level'], 5)
