from django.contrib import admin
from .models import Exercise, ExerciseCategory

admin.site.register(ExerciseCategory)
admin.site.register(Exercise)
