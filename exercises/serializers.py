from rest_framework import serializers
from .models import ExerciseCategory, Exercise

class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ['category_id', 'name']

class ExerciseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ExerciseCategory.objects.all())
    category_detail = ExerciseCategorySerializer(source='category', read_only=True)

    class Meta:
        model = Exercise
        fields = ['exercise_id', 'category', 'category_detail', 'user', 'name', 'description', 'image']
        read_only_fields = ['user']  # User is set automatically in the view
