from django.urls import path
from . import views

urlpatterns = [
    path('scoring-get', views.get_scoring, name='get_scoring'),
    path('scoring-level', views.get_level, name='get_level'),
]
