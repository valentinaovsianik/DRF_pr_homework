from django.core.management.base import BaseCommand
from users.models import Payment, User
from materials.models import Course, Lesson
from decimal import Decimal
from random import choice, randint


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Создаем тестовые курсы
        course1 = Course.objects.create(
            title="Python для начинающих",
            description="Курс для изучения основ Python.",
        )
        course2 = Course.objects.create(
            title="Django для продвинутых",
            description="Курс для изучения Django.",
        )

        # Создаем тестовые уроки
        lesson1 = Lesson.objects.create(
            title="Урок 1: Введение в Python",
            description="Описание урока 1.",
            course=course1,
        )
        lesson2 = Lesson.objects.create(
            title="Урок 2: Работа с моделями в Django",
            description="Описание урока 2.",
            course=course2,
        )

        # Получаем существующих пользователей
        users = User.objects.all()
        if users.count() < 4:
            self.stderr.write(self.style.ERROR("Недостаточно пользователей для создания платежей."))
            return

        # Создаем тестовые платежи
        Payment.objects.create(
            user=users[0],
            course=course1,
            lesson=lesson1,
            amount=5000.00,
            payment_method=Payment.CASH,
        )
        Payment.objects.create(
            user=users[1],
            course=course2,
            lesson=lesson2,
            amount=7500.00,
            payment_method=Payment.TRANSFER,
        )
        Payment.objects.create(
            user=users[2],
            course=course1,
            lesson=None,
            amount=10000.00,
            payment_method=Payment.CASH,
        )
        Payment.objects.create(
            user=users[3],
            course=None,
            lesson=lesson2,
            amount=3000.00,
            payment_method=Payment.TRANSFER,
        )

        self.stdout.write(self.style.SUCCESS("Тестовые платежи успешно созданы!"))
