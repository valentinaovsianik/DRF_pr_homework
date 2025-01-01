from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.apps import MaterialsConfig

from .views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView, LessonRetrieveView,
                    LessonUpdateView, SubscriptionView)

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="lessons_create"),
    path("lessons/<int:pk>/", LessonRetrieveView.as_view(), name="lessons_retrieve"),
    path("lessons/<int:pk>/update/", LessonUpdateView.as_view(), name="lessons_update"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lessons_delete"),
    path("subscribe/", SubscriptionView.as_view(), name="subscribe"),
]

urlpatterns += router.urls
