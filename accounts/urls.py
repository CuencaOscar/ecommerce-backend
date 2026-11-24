from django.urls import path
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

auth_tag = extend_schema_view(post=extend_schema(tags=["auth"]))

urlpatterns = [
    path("register/", views.register, name="register"),
    # Sign in with {"username": "<email>", "password": "..."}.
    path("token/", auth_tag(TokenObtainPairView).as_view(), name="token-obtain"),
    path("token/refresh/", auth_tag(TokenRefreshView).as_view(), name="token-refresh"),
    path("me/", views.me, name="me"),
]
