from django.urls import path
from . import views

urlpatterns = [
    path('training-get', views.get_training, name='get_training'),
    path('training-create', views.create_training, name='create_training'),
    path('training-start', views.start_training, name='start_training'),
    path('training-edit', views.edit_training, name='edit_training'),
    path('training-save', views.save_training, name='save_training'),
]
