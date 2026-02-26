from rest_framework import serializers
from .models import Scoring, LevelCurrent

class ScoringSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Scoring
        fields = ['scoring_id', 'user', 'username', 'value', 'created_at']

class LevelCurrentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    level = serializers.SerializerMethodField()
    xp_current = serializers.SerializerMethodField()
    xp_needed = serializers.SerializerMethodField()
    
    class Meta:
        model = LevelCurrent
        fields = ['level_id', 'user', 'username', 'level', 'xp', 'xp_current', 'xp_needed']
    
    def get_level(self, obj):
        """Get calculated level based on XP"""
        return obj.get_level()
    
    def get_xp_current(self, obj):
        """XP within current level"""
        return obj.get_current_level_xp()
    
    def get_xp_needed(self, obj):
        """Total XP needed for next level"""
        return obj.get_xp_needed_for_next_level()

