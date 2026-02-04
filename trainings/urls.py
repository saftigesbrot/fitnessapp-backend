from django.urls import path
from . import views

urlpatterns = [
    path('training-get', views.get_training, name='get_training'),
    path('training-search', views.search_training, name='search_training'),
    path('training-categories', views.get_training_categories, name='get_training_categories'),
    path('training-create', views.create_training, name='create_training'),
    path('training-start', views.start_training, name='start_training'),
    path('training-edit', views.edit_training, name='edit_training'),
    path('training-save', views.save_training_execution, name='save_training'),
    path('training-last-executed', views.get_last_executed_plan, name='get_last_executed_plan'),
]

