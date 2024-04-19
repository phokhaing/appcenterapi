from rest_framework import serializers

from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        depth = 1

    def validate_name_en(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Department name en must be greater than 5 characters!")
        return value

    def validate_name_kh(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Department name kh must be greater than 5 characters!")
        return value
