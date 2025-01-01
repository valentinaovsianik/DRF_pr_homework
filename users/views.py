from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from .models import Course, Payment, User
from .serializers import PaymentSerializer, UserSerializer
from .services import create_stripe_price, create_stripe_product, create_stripe_session


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    """CRUD для регистрации пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentsViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
    ordering_fields = [
        "payment_date",
    ]


class PaymentCreateView(APIView):
    """Оплата курса через Stripe"""

    def post(self, request, *args, **kwargs):
        course_id = request.data.get("course_id")
        amount = request.data.get("amount")

        if not course_id or not amount:
            return Response(
                {"error": "course_id и amount обязательны для указания"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            course = get_object_or_404(Course, id=course_id)

            # Создание продукта и цены в Stripe
            product_id = create_stripe_product(course)
            price_id = create_stripe_price(product_id, amount)

            session_id, payment_url = create_stripe_session(price_id)

            # Сохранение платежа
            payment = Payment.objects.create(
                course=course,
                user=request.user,
                amount=amount,
                stripe_session_id=session_id,
                payment_url=payment_url,
            )

            return Response({"session_id": session_id, "payment_url": payment_url}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"error": f"Внутренняя ошибка сервера: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
