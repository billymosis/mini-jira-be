from django.contrib.auth.models import Group
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework.fields import ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "full_name", "avatar"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar",
            "last_seen",
            "is_admin",
            "is_member",
            "full_name",
        ]
        read_only_fields = ["id", "last_seen", "is_admin", "is_member", "full_name"]


class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(default=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_admin",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }

    # Use built in django create
    def create(self, validated_data):
        is_admin = validated_data.pop("is_admin", False)
        user = CustomUser.objects.create_user(**validated_data)

        if is_admin:
            admin_group, _ = Group.objects.get_or_create(name="Admins")
            user.is_staff = True
            user.is_superuser = True
            user.groups.add(admin_group)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Avatar upload example",
            description="Upload an avatar image",
            value={"avatar": "<binary file data>"},
            request_only=True,
            media_type="multipart/form-data",
        )
    ]
)
class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("avatar",)

    def validate_avatar(self, value):
        valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        if not any(value.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError("Unsupported file extension.")
        return value
