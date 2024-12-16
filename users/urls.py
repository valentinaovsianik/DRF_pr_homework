from rest_framework.routers import SimpleRouter
from django.urls import path

from users.apps import UsersConfig

from .views import PaymentsViewSet, UserViewSet, UserCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name

router = SimpleRouter()
router.register(r"user", UserViewSet, basename="user")
router.register(r"payments", PaymentsViewSet, basename="payment")

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
