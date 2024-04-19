from rest_framework import serializers
from .models import LeaveReasonModel

from ...user_management.serializer.user import UserListingSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveReasonModel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = UserListingSerializer(
                created_by).data

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = UserListingSerializer(
                updated_by).data

        return representation
