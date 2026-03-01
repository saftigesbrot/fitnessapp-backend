import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fitness_backend.settings")
django.setup()

from trainings.serializers import TrainingPlanSerializer
from rest_framework.exceptions import ValidationError

data = {
    'name': 'g',
    'description': 'Created via App',
    'category': 101,  # typical dummy ID
    'public': False,
    'break_time': 60,
    'order': [1, 2]
}

s = TrainingPlanSerializer(data=data)
print("Is Valid?:", s.is_valid())
if not s.is_valid():
    print("Errors:", s.errors)
