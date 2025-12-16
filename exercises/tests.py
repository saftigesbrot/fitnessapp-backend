from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ExerciseCategory, Exercise
from django.core.files.uploadedfile import SimpleUploadedFile
import io
from PIL import Image

class ExerciseTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = ExerciseCategory.objects.create(name='Cardio')
        
        # Create a dummy image
        image_file = io.BytesIO()
        image = Image.new('RGB', (100, 100), 'white')
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        self.image = SimpleUploadedFile("test_image.jpg", image_file.read(), content_type="image/jpeg")

    def test_create_exercise(self):
        data = {
            'category': self.category.category_id,
            'name': 'Running',
            'description': 'Run fast',
            'image': self.image
        }
        response = self.client.post('/exercise-create', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Exercise.objects.get().name, 'Running')

    def test_get_exercise(self):
        exercise = Exercise.objects.create(
            category=self.category,
            user=self.user,
            name='Swimming',
            description='Swim laps',
            image=self.image
        )
        response = self.client.get(f'/exercise-get?id={exercise.exercise_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Swimming')

    def test_search_exercises(self):
        Exercise.objects.create(
            category=self.category,
            user=self.user,
            name='Swimming',
            description='Swim laps',
            image=self.image
        )
        # Search by name
        response = self.client.get('/exercise-search?name=Swim')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # Search by category
        response = self.client.get('/exercise-search?category=Cardio')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Search by non-existent name
        response = self.client.get('/exercise-search?name=Yoga')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
