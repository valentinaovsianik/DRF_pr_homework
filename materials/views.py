from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsNotModerator


class CourseViewSet(ModelViewSet):  # Используем ViewSet для реализации всех операций с моделью Курса
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Ограничение доступа для модератора"""
        if self.action in ["create", "destroy"]:
            # Запрещаем модераторам создание и удаление
            self.permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["update", "partial_update", "retrieve", "list"]:
            # Разрешаем просмотр и редактирование модераторам
            self.permission_classes = [IsAuthenticated, IsModerator]
        return [permission() for permission in self.permission_classes]


# CRUD для модели урока через Generic-классы
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]
