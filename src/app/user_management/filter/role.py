from django_filters import rest_framework as filters
from ..models import Role


class RoleFilter(filters.FilterSet):
    class Meta:
        model = Role
        fields = ("id", "role_name_en", "role_name_kh", "description", "is_active")