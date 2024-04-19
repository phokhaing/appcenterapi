from django_filters import rest_framework as filters
from .models import EmailHook, EmailLanguage, EmailTemplate, Notification
from app.user_management.models import User


class EmailHookFilter(filters.FilterSet):
    class Meta:
        model = EmailHook
        fields = (
            "id",
            "hook",
            "hook_name",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        )


class EmailLanguageFilter(filters.FilterSet):
    class Meta:
        model = EmailLanguage
        fields = (
            "id",
            "title",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        )


class EmailTemplateFilter(filters.FilterSet):
    class Meta:
        model = EmailTemplate
        fields = (
            "id",
            "title",
            "message",
            "hook",
            "language",
            "status",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
        )


class NotificationFilter(filters.FilterSet):

    class Meta:
        model = Notification
        fields = (
            "id",
            "from_user",
            "to_user",
            "module_id",
            "is_read",
        )


class UserOptionSelectFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "username",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
        )
