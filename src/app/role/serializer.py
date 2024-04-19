from rest_framework import serializers
from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
        # depth = 1

    def validate_name_en(self, value):
        if len(value) != 100:
            raise serializers.ValidationError("Role name en must be 5 characters!")
        return value

    def validate_name_kh(self, value):
        if len(value) != 100:
            raise serializers.ValidationError("Role name kh must be 5 characters!")
        return value
