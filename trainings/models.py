from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise

class TrainingCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    difficulty_level = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TrainingPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(TrainingCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    break_time = models.IntegerField(help_text="Break time in seconds")
    order = models.JSONField(help_text="JSON list of exercise IDs defining the order")

    def __str__(self):
        return self.name

class TrainingPlanScoring(models.Model):
    scoring_plan_id = models.AutoField(primary_key=True)
    use_scoring = models.BooleanField(default=True)
    # Placeholder for SCORING_ALLTIME as IntegerField per plan
    # Linked to ScoringAllTime
    scoring = models.ForeignKey('scorings.Scoring', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class TrainingPlanExercise(models.Model):
    """
    Represents a specific session/instance of a training plan being executed.
    """
    plan_exercise_id = models.AutoField(primary_key=True)
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    # The scoring is attached at the end of the session
    scoring_plan = models.ForeignKey(TrainingPlanScoring, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.JSONField(default=list, help_text="JSON list of exercise IDs defining the execution order")
    created_at = models.DateTimeField(auto_now_add=True)

class TrainingExerciseExecution(models.Model):
    """
    Represents a single set/execution of an exercise within a training session.
    """
    execution_id = models.AutoField(primary_key=True)
    # Changed relationship: Multiple executions belong to one TrainingPlanExercise (Session)
    plan_exercise = models.ForeignKey(TrainingPlanExercise, on_delete=models.CASCADE, related_name='executions')
    # Use exercise_id directly or link to Exercise model if we need to know WHICH exercise was performed here
    # The user didn't explicitly ask for an Exercise FK here, but it's crucial for understanding WHAT was done.
    # However, reliance on 'order' in Plan might be implied. Let's add Exercise FK for clarity and robustness.
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE) 
    
    weight = models.FloatField()
    duration = models.IntegerField(help_text="Duration in seconds")
    repetitions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
