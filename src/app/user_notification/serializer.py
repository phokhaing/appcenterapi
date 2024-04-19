from rest_framework import serializers
from datetime import datetime
from .models import EmailHook, EmailLanguage, EmailTemplate, Notification
from django.contrib.auth import get_user_model
from django.utils import timezone
from ..user_management.models import Module, UserAvatar
from django.conf import settings
from ..department.serializer import DepartmentSerializer
from ..position.serializer import PositionSerializer

User = get_user_model()


class EmailHookSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    updated_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = EmailHook
        fields = "__all__"

    # depth = 1

    def validate(self, data):
        if len(data.get("hook_name")) <= 3:
            raise serializers.ValidationError(
                "Email Hook name must be greater than 4 numbers!"
            )

        return data


class EmailLanguageSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    updated_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = EmailLanguage
        fields = "__all__"

    # depth = 1

    def validate(self, data):
        if len(data.get("title")) <= 3:
            raise serializers.ValidationError(
                "Email Language Title must be greater than 4 characters!"
            )

        return data


class EmailTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    updated_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )

    class Meta:
        model = EmailTemplate
        fields = "__all__"

    # depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        hook = instance.hook
        if hook:
            representation["hook"] = EmailHookSerializer(hook).data

        return representation

    def validate(self, data):
        if len(data.get("title")) <= 3:
            raise serializers.ValidationError(
                "Email Template Title must be greater than 4 characters!"
            )

        return data


class ModuleNotiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ["id", "module_name"]


class UserAvatarNotiSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, instance):
        base_url = settings.GET_MEDIA_URL
        return f"{base_url}/images/profile/{instance.upload_file_name}"

    class Meta:
        model = UserAvatar
        fields = ["url"]


class UserNotiSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(required=False)
    department = serializers.StringRelatedField(source="department.name_en")
    # position = PositionSerializer(required=False)
    position = serializers.StringRelatedField(source="position.name_en")
    avatar = UserAvatarNotiSerializer(many=True, source="attachment_files.all")

    class Meta:
        model = User
        fields = [
            "id",
            "staff_id",
            "fullname",
            "gender",
            "department",
            "position",
            "avatar",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    from_user = UserNotiSerializer(required=False)
    to_user = UserNotiSerializer(required=False)
    module_id = serializers.StringRelatedField(source="module_id.module_name")
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False)
    processing_time = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            "id",
            "from_user",
            "to_user",
            "url",
            "message",
            "record_id",
            "module_id",
            "is_read",
            "created_at",
            "processing_time",
        ]

    def get_processing_time(self, obj):
        created_at = obj.created_at
        current_time = timezone.now()
        processing_time = current_time - created_at

        # Extract days, hours, and minutes from the timedelta
        days = processing_time.days
        hours = processing_time.seconds // 3600
        minutes = (processing_time.seconds // 60) % 60

        # Return the processing time as a dictionary
        return {
            "days": days,
            "hours": hours,
            "minutes": minutes,
        }


class NotificationStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "noti_count"]


class UserListingNotiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "username",
            "email",
            "fullname",
            "position",
        )
