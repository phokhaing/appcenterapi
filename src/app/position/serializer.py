from rest_framework import serializers
from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"
        depth = 1

    def validate_name_en(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Position name en must be greater than 5 characters!")
        return value

    def validate_name_kh(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Position name kh must be greater than 5 characters!")
        return value
