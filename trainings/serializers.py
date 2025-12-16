from rest_framework import serializers
from .models import TrainingCategory, TrainingPlan, TrainingPlanExercise, TrainingExerciseExecution, TrainingPlanScoring
from exercises.serializers import ExerciseSerializer

class TrainingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCategory
        fields = '__all__'

class TrainingPlanSerializer(serializers.ModelSerializer):
    category_detail = TrainingCategorySerializer(source='category', read_only=True)

    class Meta:
        model = TrainingPlan
        fields = ['plan_id', 'user', 'category', 'category_detail', 'name', 'public', 'break_time', 'order']
        read_only_fields = ['user']

class TrainingExerciseExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingExerciseExecution
        fields = ['execution_id', 'plan_exercise', 'exercise', 'weight', 'duration', 'repetitions', 'created_at']
        read_only_fields = ['plan_exercise', 'created_at']

class TrainingPlanScoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingPlanScoring
        fields = '__all__'

class TrainingPlanExerciseSerializer(serializers.ModelSerializer):
    executions = TrainingExerciseExecutionSerializer(many=True, read_only=True)
    scoring_plan_detail = TrainingPlanScoringSerializer(source='scoring_plan', read_only=True)

    class Meta:
        model = TrainingPlanExercise
        fields = ['plan_exercise_id', 'plan', 'scoring_plan', 'scoring_plan_detail', 'executions', 'created_at']
