from django.db import models
from django.contrib.auth.models import User

class ExerciseCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    exercise_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(ExerciseCategory, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='exercises/', null=True, blank=True)

    def __str__(self):
        return self.name
