from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Создает группу Moderator"""

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Moderator")
        if created:
            self.stdout.write(self.style.SUCCESS("Группа Moderator создана"))
        else:
            self.stdout.write(self.style.WARNING("Группа Moderator уже существует"))
