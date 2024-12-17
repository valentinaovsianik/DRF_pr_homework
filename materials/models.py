from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(upload_to="courses/previews/", verbose_name="Превью", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание", default="Default description")
    preview = models.ImageField(upload_to="lessons/previews/", verbose_name="Превью", blank=True, null=True)
    video_url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, verbose_name="Владелец", blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.title} (курс: {self.course.title})"
