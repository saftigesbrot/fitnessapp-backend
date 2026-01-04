from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ExerciseCategory, Exercise
from django.core.files.uploadedfile import SimpleUploadedFile

class ExerciseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = ExerciseCategory.objects.create(name='Arms')
        
    def test_create_exercise(self):
        self.client.force_authenticate(user=self.user)
        image = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpeg")
        data = {
            'name': 'Bicep Curl',
            'description': 'Lift weight',
            'category': self.category.category_id,
            'image': image
        }
        response = self.client.post('/exercise-create', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        
    def test_get_exercise(self):
        exercise = Exercise.objects.create(
            user=self.user,
            category=self.category,
            name='Tricep Dip',
            description='Dip it',
            image='exercises/test.jpg'
        )
        response = self.client.get(f'/exercise-get?id={exercise.exercise_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Tricep Dip')

    def test_search_exercises(self):
        Exercise.objects.create(
            user=self.user,
            category=self.category,
            name='Pushups',
            description='Push it',
            image='exercises/pushups.jpg'
        )
        response = self.client.get('/exercise-search?name=Push')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category_list(self):
        # Create another category
        ExerciseCategory.objects.create(name='Legs')
        
        response = self.client.get('/category-list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Verify structure keys
        first_category = response.data[0]
        self.assertIn('id', first_category)
        self.assertIn('name', first_category)
        self.assertNotIn('category_id', first_category) # Should use 'id'
