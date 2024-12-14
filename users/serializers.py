from rest_framework import serializers

from .models import Payment, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели платежа"""

    class Meta:
        model = Payment
        fields = "__all__"
