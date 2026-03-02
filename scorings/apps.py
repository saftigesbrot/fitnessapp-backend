from django.apps import AppConfig


class ScoringsConfig(AppConfig):
    name = 'scorings'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        """Import signals when app is ready"""
        import scorings.signals
