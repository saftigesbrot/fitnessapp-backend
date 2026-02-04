from rest_framework import serializers
from .models import Scoring, LevelCurrent

class ScoringSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Scoring
        fields = '__all__'

class LevelCurrentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = LevelCurrent
        fields = ['level_id', 'user', 'username', 'level', 'xp']
