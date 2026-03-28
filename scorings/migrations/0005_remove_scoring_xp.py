# Generated migration

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorings', '0004_auto_level_from_xp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scoring',
            name='xp',
        ),
    ]
