from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User
from exercises.models import Exercise, ExerciseCategory
from trainings.models import TrainingPlan, TrainingCategory
from scorings.models import Scoring, LevelCurrent


class Command(BaseCommand):
    help = 'Lädt Test-Daten (User, Übungen, Kategorien, Scores) in die Datenbank'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Löscht zuerst alle bestehenden Daten',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Lösche bestehende Daten...'))
            
            # Lösche Daten in der richtigen Reihenfolge (wegen Foreign Keys)
            LevelCurrent.objects.all().delete()
            Scoring.objects.all().delete()
            TrainingPlan.objects.all().delete()
            TrainingCategory.objects.all().delete()
            Exercise.objects.all().delete()
            ExerciseCategory.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            
            self.stdout.write(self.style.SUCCESS('✓ Daten gelöscht'))

        self.stdout.write(self.style.MIGRATE_HEADING('📦 Lade Test-Daten...'))
        
        try:
            # Lade die Fixtures
            call_command('loaddata', 'fixtures/initial_data.json', verbosity=0)
            
            # Setze korrekte Passwörter für Test-User
            test_users = [
                ('admin', 'admin123'),
                ('max_mustermann', 'test123'),
                ('sarah_schmidt', 'test123'),
                ('tom_mueller', 'test123'),
                ('lisa_wagner', 'test123'),
                ('jan_fischer', 'test123'),
            ]
            
            for username, password in test_users:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                except User.DoesNotExist:
                    pass
            
            self.stdout.write(self.style.SUCCESS('\n✅ Test-Daten erfolgreich geladen!\n'))
            
            # Zeige Statistiken
            self.stdout.write(self.style.SUCCESS(f'👥 User: {User.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'📂 Übungskategorien: {ExerciseCategory.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'💪 Übungen: {Exercise.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'📂 Trainingskategorien: {TrainingCategory.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'📋 Trainingspläne: {TrainingPlan.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'🏆 Scores: {Scoring.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'⭐ Level: {LevelCurrent.objects.count()}'))
            
            self.stdout.write('\n' + self.style.MIGRATE_LABEL('Test-User (alle mit Passwort "test123"):'))
            for user in User.objects.filter(is_superuser=False):
                self.stdout.write(f'  • {user.username} ({user.first_name} {user.last_name})')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Fehler beim Laden der Daten: {str(e)}'))
            raise
