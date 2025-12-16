from django.contrib import admin
from .models import TrainingCategory, TrainingPlan, TrainingPlanExercise, TrainingExerciseExecution, TrainingPlanScoring

admin.site.register(TrainingCategory)
admin.site.register(TrainingPlan)
admin.site.register(TrainingPlanExercise)
admin.site.register(TrainingExerciseExecution)
admin.site.register(TrainingPlanScoring)
