from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="first_name", read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "name"]


class RegisterSerializer(serializers.Serializer):
    """Create a customer account. The email is also used as the username."""

    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return email

    def validate(self, attrs):
        candidate = User(username=attrs["email"], email=attrs["email"], first_name=attrs["name"])
        validate_password(attrs["password"], user=candidate)
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
            first_name=validated_data["name"],
            password=validated_data["password"],
        )
