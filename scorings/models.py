from django.db import models
from django.contrib.auth.models import User

class Scoring(models.Model):
    scoring_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Score: {self.value}"

class LevelCurrent(models.Model):
    level_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)  # Total XP accumulated

    def __str__(self):
        return f"{self.user.username} - Level: {self.level}"
    
    @staticmethod
    def xp_for_level(level):
        """Calculate total XP required to reach a specific level (logarithmic growth)"""
        if level <= 1:
            return 0
        # Logarithmic formula: base_xp * level^1.5
        # Level 2: ~141 XP, Level 3: ~260 XP, Level 4: ~400 XP, Level 5: ~559 XP, etc.
        base_xp = 100
        return int(base_xp * (level ** 1.5))
    
    def get_current_level_xp(self):
        """Get XP within current level (for progress bar)"""
        xp_for_current_level = self.xp_for_level(self.level)
        xp_for_next_level = self.xp_for_level(self.level + 1)
        xp_in_current_level = self.xp - xp_for_current_level
        return max(0, xp_in_current_level)
    
    def get_xp_needed_for_next_level(self):
        """Get total XP needed to reach next level from current level start"""
        xp_for_current_level = self.xp_for_level(self.level)
        xp_for_next_level = self.xp_for_level(self.level + 1)
        return xp_for_next_level - xp_for_current_level
    
    def check_and_level_up(self):
        """Check if user should level up and update accordingly"""
        while self.xp >= self.xp_for_level(self.level + 1):
            self.level += 1
        self.save()

