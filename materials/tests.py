from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.owner = User.objects.create(email="owner@example.com", password="password123")
        self.user = User.objects.create(email="user@example.com", password="password123")

        # Создание курса
        self.course = Course.objects.create(title="Тестовый курс", description="Описание курса", owner=self.owner)

        # Создание урока
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание урока",
            course=self.course,
            owner=self.owner,
        )

        # URL-ы для API
        self.lesson_list_url = "/materials/lessons/"
        self.lesson_create_url = "/materials/lessons/create/"
        self.lesson_detail_url = f"/materials/lessons/{self.lesson.id}/"
        self.lesson_update_url = f"/materials/lessons/{self.lesson.id}/update/"
        self.lesson_delete_url = f"/materials/lessons/{self.lesson.id}/delete/"
        self.subscription_url = "/materials/subscribe/"

    def test_lesson_list(self):
        """Проверка получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Не удалось получить список уроков.")
        self.assertEqual(len(response.data["results"]), 1, "Количество уроков в списке некорректно.")

    def test_lesson_create(self):
        """Проверка создания урока"""
        self.client.force_authenticate(user=self.owner)  # Убедимся, что пользователь — владелец курса
        data = {
            "title": "Новый урок",
            "description": "Описание нового урока",
            "video_url": "https://youtube.com/test",
            "course": self.course.id,
            "owner": self.owner.id,
        }
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Не удалось создать урок.")
        self.assertTrue(Lesson.objects.filter(title="Новый урок").exists())

    def test_lesson_retrieve(self):
        """Проверка получения деталей урока"""
        self.client.force_authenticate(user=self.owner)  # Убедимся, что пользователь имеет доступ к уроку
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Не удалось получить детали урока.")
        self.assertEqual(response.data["title"], self.lesson.title, "Название урока некорректно.")

    def test_lesson_update(self):
        """Проверка обновления урока"""
        self.client.force_authenticate(user=self.owner)
        data = {"title": "Обновленное название"}
        response = self.client.patch(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Не удалось обновить урок.")
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Обновленное название", "Название урока не обновлено.")

    def test_lesson_delete(self):
        """Проверка удаления урока"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, "Не удалось удалить урок.")
        self.assertEqual(Lesson.objects.count(), 0, "Урок не был удален.")

    def test_subscription_create_and_delete(self):
        """Проверка создания и удаления подписки."""
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}

        # Создание подписки
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Не удалось создать подписку.")
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists(), "Подписка не создана."
        )

        # Удаление подписки
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, "Не удалось удалить подписку.")
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists(), "Подписка не удалена."
        )
