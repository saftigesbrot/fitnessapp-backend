from django.db import models
from django.contrib.auth.models import User

class Scoring(models.Model):
    scoring_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField(default=1000)  # Points/Score (0-2000, balanced at 1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.value}"
    
    def get_progress(self):
        """Get progress as percentage (0-1) where 2000 is max"""
        return min(max(self.value / 2000, 0), 1)

class LevelCurrent(models.Model):
    level_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)  # Total XP accumulated

    def __str__(self):
        return f"{self.user.username} - Level: {self.get_level()}, XP: {self.xp}"
    
    @staticmethod
    def xp_for_level(level):
        """Calculate total XP required to reach a specific level (logarithmic growth)"""
        if level <= 1:
            return 0
        # Logarithmic formula: base_xp * level^1.5
        # Level 2: ~141 XP, Level 3: ~260 XP, Level 4: ~400 XP, Level 5: ~559 XP, etc.
        base_xp = 100
        return int(base_xp * (level ** 1.5))
    
    @staticmethod
    def calculate_level_from_xp(xp):
        """Calculate what level corresponds to given XP"""
        if xp <= 0:
            return 1
        
        level = 1
        while LevelCurrent.xp_for_level(level + 1) <= xp:
            level += 1
        return level
    
    def get_level(self):
        """Get current level based on XP (calculated, not stored)"""
        return self.calculate_level_from_xp(self.xp)
    
    @property
    def level(self):
        """Property to get level (for backwards compatibility)"""
        return self.get_level()
    
    def get_current_level_xp(self):
        """Get XP within current level (for progress bar)"""
        level = self.get_level()
        xp_for_current_level = self.xp_for_level(level)
        xp_in_current_level = self.xp - xp_for_current_level
        return max(0, xp_in_current_level)
    
    def get_xp_needed_for_next_level(self):
        """Get total XP needed to reach next level from current level start"""
        level = self.get_level()
        xp_for_current_level = self.xp_for_level(level)
        xp_for_next_level = self.xp_for_level(level + 1)
        return xp_for_next_level - xp_for_current_level
    
    def add_xp(self, amount):
        """Add XP to user (level is automatically calculated)"""
        self.xp += amount
        self.save()

