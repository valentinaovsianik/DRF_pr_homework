from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    """Асинхронная задача для отправки сообщения об обновлении курса"""
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course).select_related("user")
        user_emails = [subscription.user.email for subscription in subscriptions if subscription.user.email]
        if user_emails:
            subject = f"Обновления курса: {course.title}"
            message = f"Инфофрмируем вс, что курс '{course.title}' был обновлен."
            from_email = settings.DEFAULT_FROM_EMAIL

            # Отправка email
            send_mail(subject, message, from_email, user_emails)
    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."
    except Exception as e:
        return f"Ошибка при отправке email: {str(e)}"
