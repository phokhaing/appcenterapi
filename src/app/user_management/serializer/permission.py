from rest_framework import serializers
from ..models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = "__all__"
        # depth = 1

    _length: int = 100

    def validate_permission_name(self, value):
        if len(value) > self._length:
            raise serializers.ValidationError(
                f"Permission name en can't greater then {self._length} characters."
            )
        return value