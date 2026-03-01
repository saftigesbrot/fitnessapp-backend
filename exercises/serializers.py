from rest_framework import serializers
from .models import ExerciseCategory, Exercise

class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ['category_id', 'name']

class ExerciseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ExerciseCategory.objects.all())
    category_detail = ExerciseCategorySerializer(source='category', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Exercise
        fields = ['exercise_id', 'category', 'category_detail', 'user', 'username', 'name', 'description', 'tracking_type', 'image', 'public']
        read_only_fields = ['user']  # User is set automatically in the view

class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='category_id')
    
    class Meta:
        model = ExerciseCategory
        fields = ['id', 'name']
