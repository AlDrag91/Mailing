from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Добавляет админа"""
        user = User.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True,
            country='Admin'
        )

        user.set_password('qwerty123')
        user.save()

        """Добавляет модератора"""
        user = User.objects.create(
            email='manager@sky.pro',
            first_name='manager',
            last_name='manager',
            is_staff=True,
            is_superuser=False,
            country='manager'
        )

        user.set_password('qwerty123')
        user.save()

        """Добавляет пользователя сервиса"""
        user = User.objects.create(
            email='user_service@sky.pro',
            first_name='user_service',
            last_name='user_service',
            is_staff=True,
            is_superuser=False,
            country='user_service'
        )

        user.set_password('qwerty123')
        user.save()
