# Generated migration for automatic level calculation from XP

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorings', '0003_delete_scoringalltime_delete_scoringcurrent_and_more'),
    ]

    operations = [
        # Add XP field to Scoring model
        migrations.AddField(
            model_name='scoring',
            name='xp',
            field=models.IntegerField(default=0),
        ),
        # Remove level field from LevelCurrent (it's now calculated)
        migrations.RemoveField(
            model_name='levelcurrent',
            name='level',
        ),
    ]
