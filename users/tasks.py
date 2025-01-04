from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import User


@shared_task
def deactivate_inactive_users():
    """Блокирует пользователей, не заходивших больше месяца"""
    one_month_ago = now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(last_login__lt=one_month_ago, is_active=True)
    for user in users_to_deactivate:
        user.is_active = False
        user.save()
    return f"Деактивировано {users_to_deactivate.count()} пользователей."