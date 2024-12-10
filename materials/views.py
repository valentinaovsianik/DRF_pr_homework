from rest_framework.viewsets import ModelViewSet
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView



class CourseViewSet(ModelViewSet):  # Используем ViewSet для реализации всех операций с моделью Курса
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# CRUD для модели урока через Generic-классы
class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonListCreateAPIView(ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
