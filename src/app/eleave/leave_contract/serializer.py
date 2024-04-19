from rest_framework import serializers

from .models import LeaveContractModel
from ..leave_type.models import LeaveTypeModel
from ..leave_type.serializer import LeaveTypeSerializer

from ...user_management.serializer.user import UserListingSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveContractSerializer(serializers.ModelSerializer):
    # Modify the default_leave_type field to accept integers and strings

    # created_by = serializers.StringRelatedField(
    #     default=serializers.CurrentUserDefault(), read_only=True)
    # updated_by = serializers.StringRelatedField(
    #     default=serializers.CurrentUserDefault(), read_only=True)

    default_leave_type = serializers.CharField(write_only=True)

    class Meta:
        model = LeaveContractModel
        fields = "__all__"

    def validate_name(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Field name allow min lenght 5 characters!"
            )
        return value

    def validate_day_start(self, value):
        if int(value) > 31:
            raise serializers.ValidationError(
                "Field day start allow max value 31 only."
            )
        return value

    def validate_month_start(self, value):
        if int(value) > 12:
            raise serializers.ValidationError(
                "Field day start allow max value 12 only")
        return value

    def validate_default_leave_type(self, value):
        # Check if the value is an integer or a numeric string
        if isinstance(value, int):
            leave_type_id = value
        elif str(value).isdigit():  # Check if it's a numeric string
            leave_type_id = int(value)
        else:
            raise serializers.ValidationError("Invalid leave_type value.")

        try:
            leave_type = LeaveTypeModel.objects.get(id=leave_type_id)
        except LeaveTypeModel.DoesNotExist:
            raise serializers.ValidationError("Invalid leave_type ID.")

        return leave_type

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fetch the related LeaveTypeModel object and serialize it
        default_leave_type = instance.default_leave_type
        if default_leave_type:
            representation["default_leave_type"] = LeaveTypeSerializer(
                default_leave_type
            ).data

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = UserListingSerializer(
                created_by).data

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = UserListingSerializer(
                updated_by).data

        return representation
