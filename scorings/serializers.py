from rest_framework import serializers
from .models import ScoringCurrent, ScoringTop, ScoringAllTime, LevelCurrent

class ScoringCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringCurrent
        fields = '__all__'

class ScoringTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringTop
        fields = '__all__'

class ScoringAllTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoringAllTime
        fields = '__all__'

class LevelCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelCurrent
        fields = ['level_id', 'user', 'level', 'xp']
