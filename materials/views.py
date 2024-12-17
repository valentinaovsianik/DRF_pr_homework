from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):  # Используем ViewSet для реализации всех операций с моделью Курса
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Ограничение доступа для модератора и владельца"""
        if self.action == "create":
            self.permission_classes = (IsAuthenticated, ~IsModerator)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsAuthenticated, IsOwner | IsModerator)
        elif self.action == "destroy":
            self.permission_classes = (IsAuthenticated, IsOwner)
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):  # Привязка владельца при создании курса
        serializer.save(owner=self.request.user)


# CRUD для модели урока через Generic-классы
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):  # Привязка владельца при создании урока
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]
