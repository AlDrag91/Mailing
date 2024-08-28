from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
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
