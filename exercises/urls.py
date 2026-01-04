from django.urls import path
from . import views

urlpatterns = [
    path('exercise-get', views.get_exercise, name='get_exercise'),
    path('exercise-create', views.create_exercise, name='create_exercise'),
    path('exercise-search', views.search_exercises, name='search_exercises'),
    path('category-list', views.get_category_list, name='get_category_list'),
]
