from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


urlpatterns = [
    path("signup", views.Signup.as_view()),
    path("logout", views.Logout.as_view()),
    path("login/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]