from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Scoring, LevelCurrent

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_scoring_and_level(sender, instance, created, **kwargs):
    """
    Automatically create Scoring and LevelCurrent entries for new users.
    - Scoring: 1000 points (balanced starting point)
    - LevelCurrent: 0 XP (Level 1)
    """
    if created:
        # Create Scoring entry with balanced 1000 points
        Scoring.objects.create(
            user=instance,
            value=1000  # Balanced starting point
        )
        
        # Create LevelCurrent entry with 0 XP
        LevelCurrent.objects.create(
            user=instance,
            xp=0  # Starting at Level 1 with 0 XP
        )
