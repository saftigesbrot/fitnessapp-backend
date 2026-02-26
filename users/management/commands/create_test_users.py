from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from scorings.models import Scoring, LevelCurrent
from django.utils import timezone


class Command(BaseCommand):
    help = 'Creates test users with proper passwords'

    def handle(self, *args, **options):
        # Delete existing test users (except admin if exists)
        User.objects.filter(username__in=[
            'max_mustermann', 'sarah_schmidt', 'tom_mueller', 
            'lisa_wagner', 'jan_fischer'
        ]).delete()

        self.stdout.write('Creating test users...')

        # Admin user
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@fitness.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'first_name': 'Admin',
                'last_name': 'User'
            }
        )
        if created or not admin.has_usable_password():
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user'))

        # Create admin scoring and level data
        Scoring.objects.get_or_create(
            user=admin,
            defaults={
                'value': 1600,  # Very good
                'created_at': timezone.now()
            }
        )
        LevelCurrent.objects.get_or_create(
            user=admin,
            defaults={'xp': 2500}
        )

        # Test users data
        users_data = [
            {
                'username': 'max_mustermann',
                'email': 'max@fitness.com',
                'first_name': 'Max',
                'last_name': 'Mustermann',
                'scoring_value': 1450,  # Above average
                'level_xp': 1450
            },
            {
                'username': 'sarah_schmidt',
                'email': 'sarah@fitness.com',
                'first_name': 'Sarah',
                'last_name': 'Schmidt',
                'scoring_value': 1800,  # Excellent
                'level_xp': 2100
            },
            {
                'username': 'tom_mueller',
                'email': 'tom@fitness.com',
                'first_name': 'Tom',
                'last_name': 'Mueller',
                'scoring_value': 850,  # Below average
                'level_xp': 850
            },
            {
                'username': 'lisa_wagner',
                'email': 'lisa@fitness.com',
                'first_name': 'Lisa',
                'last_name': 'Wagner',
                'scoring_value': 1200,  # Above average
                'level_xp': 1200
            },
            {
                'username': 'jan_fischer',
                'email': 'jan@fitness.com',
                'first_name': 'Jan',
                'last_name': 'Fischer',
                'scoring_value': 650,  # Below average
                'level_xp': 650
            }
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True
                }
            )
            user.set_password('test123')
            user.save()

            # Create scoring data
            Scoring.objects.get_or_create(
                user=user,
                defaults={
                    'value': user_data['scoring_value'],
                    'created_at': timezone.now()
                }
            )

            # Create level data
            LevelCurrent.objects.get_or_create(
                user=user,
                defaults={'xp': user_data['level_xp']}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated user: {user.username}'))

        self.stdout.write(self.style.SUCCESS('\nAll test users created successfully!'))
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('  admin / admin123 (Superuser)')
        self.stdout.write('  max_mustermann / test123')
        self.stdout.write('  sarah_schmidt / test123')
        self.stdout.write('  tom_mueller / test123')
        self.stdout.write('  lisa_wagner / test123')
        self.stdout.write('  jan_fischer / test123')
