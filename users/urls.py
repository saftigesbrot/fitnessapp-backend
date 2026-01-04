from django.urls import path
from . import views

urlpatterns = [
    path('user-get', views.get_user, name='get_user'),
]
