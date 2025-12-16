from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import TrainingCategory, TrainingPlan, TrainingPlanExercise, TrainingExerciseExecution
from exercises.models import Exercise, ExerciseCategory

class TrainingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        self.cat = TrainingCategory.objects.create(name='Strength', difficulty_level='Hard')
        self.ex_cat = ExerciseCategory.objects.create(name='Arms')
        self.exercise = Exercise.objects.create(category=self.ex_cat, user=self.user, name='Bicep Curl', description='Curl it')

    def test_create_and_get_plan(self):
        data = {
            'user': self.user.id, # Should be ignored by serializer read_only, but good to check
            'category': self.cat.category_id,
            'name': 'Arm Day',
            'public': False,
            'break_time': 60,
            'order': [self.exercise.exercise_id]
        }
        response = self.client.post('/training-create', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plan_id = response.data['plan_id']
        
        # Get query
        response = self.client.get(f'/training-get?id={plan_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Arm Day')

    def test_start_and_save_training(self):
        # 1. Create Plan
        plan = TrainingPlan.objects.create(
            user=self.user,
            category=self.cat,
            name='Leg Day',
            public=True,
            break_time=90,
            order=[]
        )
        
        # 2. Start Training (Create Session)
        response = self.client.post('/training-start', {'plan_id': plan.plan_id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        plan_exercise_id = response.data['plan_exercise_id']
        
        # 3. Save Training
        save_data = {
            'plan_exercise_id': plan_exercise_id,
            'scoring': {'use_scoring': True, 'scoring_id': 100},
            'executions': [
                {'exercise_id': self.exercise.exercise_id, 'weight': 20, 'duration': 0, 'repetitions': 12},
                {'exercise_id': self.exercise.exercise_id, 'weight': 20, 'duration': 0, 'repetitions': 10}
            ]
        }
        response = self.client.post('/training-save', save_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify DB
        session = TrainingPlanExercise.objects.get(plan_exercise_id=plan_exercise_id)
        self.assertIsNotNone(session.scoring_plan)
        self.assertEqual(session.scoring_plan.scoring_id, 100)
        
        executions = TrainingExerciseExecution.objects.filter(plan_exercise=session)
        self.assertEqual(executions.count(), 2)
        self.assertEqual(executions[0].weight, 20)
