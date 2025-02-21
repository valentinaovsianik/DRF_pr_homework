from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsModerator, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import CustomPagination
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_email


@method_decorator(name="list", decorator=swagger_auto_schema(operation_description="Course ViewSet"))
class CourseViewSet(ModelViewSet):  # Используем ViewSet для реализации всех операций с моделью Курса
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

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

    def perform_update(self, serializer):
        """Добавление асинхронной задачи после обновления курса"""
        course = serializer.save()
        # Запуск задачи отправки email подписчикам курса
        send_course_update_email.delay(course.id)


# CRUD для модели урока через Generic-классы
class LessonCreateAPIView(CreateAPIView):
    """Lesson create"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):  # Привязка владельца при создании урока
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """Lesson list"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveView(RetrieveAPIView):
    """Lesson retrieve"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateView(UpdateAPIView):
    """Lesson update"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """Lesson destroy"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | ~IsModerator]


class SubscriptionView(APIView):
    """Subscription view"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем объекты подписок по текущему пользователю и курса
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():  # Если подписка уже существует, удаляем ее
            subs_item.delete()
            message = "Подписка удалена."
        else:  # Если подписки нет, создаем ее
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена."

        return Response({"message": message}, status=status.HTTP_200_OK)
