from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from scorings.models import LevelCurrent

User = get_user_model()


class Command(BaseCommand):
    help = 'Add test XP to a user for testing level-up functionality'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to add XP to')
        parser.add_argument('xp', type=int, help='Amount of XP to add')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
            level_obj, created = LevelCurrent.objects.get_or_create(user=user)
            
            old_level = level_obj.get_level()
            old_xp = level_obj.xp
            
            level_obj.add_xp(options['xp'])
            
            new_level = level_obj.get_level()
            new_xp = level_obj.xp
            
            self.stdout.write(self.style.SUCCESS('✅ XP erfolgreich hinzugefügt!'))
            self.stdout.write(f"User: {user.username}")
            self.stdout.write(f"XP: {old_xp} → {new_xp} (+{options['xp']})")
            self.stdout.write(f"Level: {old_level} → {new_level}")
            
            if new_level > old_level:
                self.stdout.write(self.style.WARNING(f"🎉 LEVEL UP! Von Level {old_level} auf Level {new_level}!"))
            
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ User "{options["username"]}" nicht gefunden!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Fehler: {str(e)}'))
