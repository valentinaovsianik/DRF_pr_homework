from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import CourseViewSet, LessonListCreateAPIView, LessonCreateAPIView, LessonRetrieveView, LessonUpdateView, LessonDestroyAPIView
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListCreateAPIView.as_view(), name="lessons_list_create"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/", LessonRetrieveView.as_view(), name="lessons_retrieve"),
    path("lessons/<int:pk>/update/", LessonUpdateView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
]

urlpatterns += router.urls