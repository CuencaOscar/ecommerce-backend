from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import permissions, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, UserSerializer


def _tokens_for(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@extend_schema(
    tags=["auth"],
    auth=[],
    request=RegisterSerializer,
    responses={201: inline_serializer("RegisterResponse", {
        "user": UserSerializer(), "refresh": serializers.CharField(), "access": serializers.CharField(),
    })},
)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """Create an account and return the user with a JWT pair, so the client is signed in right away."""
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"user": UserSerializer(user).data, **_tokens_for(user)}, status=status.HTTP_201_CREATED)


@extend_schema(tags=["auth"], responses=UserSerializer)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    """The signed-in user."""
    return Response(UserSerializer(request.user).data)
