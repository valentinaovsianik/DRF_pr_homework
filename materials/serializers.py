from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    video_url = serializers.URLField(validators=[YouTubeURLValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscription = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        """Возвращает количество уроков курса"""
        return obj.lessons.count()

    def get_is_subscription(self, obj):
        """Проверяет наличие подписки на курс"""
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = "__all__"
