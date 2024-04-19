from django_filters import rest_framework as filters

from ..models import Permission


class PermissionFilter(filters.FilterSet):
    class Meta:
        model = Permission
        fields = ("id", "permission_name", "description", "is_active")