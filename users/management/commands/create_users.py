from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        """Создает пользователей"""
        user1 = User(
            email="user1@example.com",
            first_name="Иван",
            last_name="Иванов",
            phone="1234567890",
            city="Москва",
        )
        user1.set_password("password123")
        user1.save()

        user2 = User(
            email="user2@example.com",
            first_name="Петр",
            last_name="Петров",
            phone="0987654321",
            city="Самара",
        )
        user2.set_password("password456")
        user2.save()

        user3 = User(
            email="user3@example.com",
            first_name="Полина",
            last_name="Мышкина",
            phone="6674567890",
            city="Москва",
        )
        user3.set_password("password789")
        user3.save()

        user4 = User(
            email="user4@example.com",
            first_name="Никита",
            last_name="Грозный",
            phone="1234567890",
            city="Ростов",
        )
        user4.set_password("password135")
        user4.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Пользователи {user1.email}, {user2.email}, {user3.email} и {user4.email} успешно созданы"
            )
        )
