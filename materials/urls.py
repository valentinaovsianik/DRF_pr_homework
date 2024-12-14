from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig

from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListCreateAPIView,
                    LessonRetrieveView, LessonUpdateView)

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
