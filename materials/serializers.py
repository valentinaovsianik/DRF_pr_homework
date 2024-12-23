from rest_framework import serializers

from .models import Course, Lesson

from .validators import YouTubeURLValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для урока"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeURLValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курса"""

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков курса"""
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = "__all__"
