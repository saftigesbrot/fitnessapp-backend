from rest_framework import serializers
from .models import TrainingCategory, TrainingPlan, TrainingPlanExercise, TrainingExerciseExecution, TrainingPlanScoring
from exercises.serializers import ExerciseSerializer

class TrainingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingCategory
        fields = '__all__'

from exercises.models import Exercise

class TrainingPlanSerializer(serializers.ModelSerializer):
    category_detail = TrainingCategorySerializer(source='category', read_only=True)
    exercises = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = TrainingPlan
        fields = ['plan_id', 'user', 'username', 'category', 'category_detail', 'name', 'public', 'break_time', 'order', 'exercises']
        read_only_fields = ['user']

    def get_exercises(self, obj):
        if not obj.order:
            return []
        
        # Ensure order is a list of IDs
        if isinstance(obj.order, list):
            exercise_ids = obj.order
            # Fetch all exercises in the list
            exercises = Exercise.objects.filter(exercise_id__in=exercise_ids)
            # Create a map for sorting
            exercise_map = {e.exercise_id: e for e in exercises}
            # Return ordered list, filtering out any missing IDs
            ordered_exercises = [exercise_map[eid] for eid in exercise_ids if eid in exercise_map]
            return ExerciseSerializer(ordered_exercises, many=True).data
        return []

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
