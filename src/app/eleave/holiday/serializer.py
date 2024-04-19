from rest_framework import serializers

from .models import HolidayModel, WeekendModel
from ..leave_contract.models import LeaveContractModel
from ..leave_contract.serializer import LeaveContractSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

class HolidaySerializer(serializers.ModelSerializer):
    default_leave_contract = serializers.CharField(write_only=True)
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    updated_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    class Meta:
        model = HolidayModel
        fields = "__all__"
        #depth = 1
    
    def validate_title(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Field validate_type allow min lenght 5 characters!"
            )
    
        return value
    def validate_default_leave_contract(self, value):
        # Check if the value is an integer or a numeric string
        if isinstance(value, int):
            leave_contract_id = value
        elif str(value).isdigit():  # Check if it's a numeric string
            leave_contract_id = int(value)
        else:
            raise serializers.ValidationError("Invalid leave_contract value.")

        try:
            leave_contract = LeaveContractModel.objects.get(id=leave_contract_id)
        except LeaveContractModel.DoesNotExist:
            raise serializers.ValidationError("Invalid leave_contract ID.")

        return leave_contract
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fetch the related LeaveTypeModel object and serialize it
        default_leave_contract = instance.default_leave_contract
        if default_leave_contract:
            representation["default_leave_contract"] = LeaveContractSerializer(
                default_leave_contract
            ).data

        return representation

class WeekendSerializer(serializers.ModelSerializer):
    default_leave_contract = serializers.CharField(write_only=True)
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    updated_by = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    class Meta:
        model = WeekendModel
        fields = "__all__"
        # depth = 1
    
    def validate_title(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError(
                "Field validate_type allow min lenght 5 characters!"
            )
    
        return value
    def validate_default_leave_contract(self, value):
        # Check if the value is an integer or a numeric string
        if isinstance(value, int):
            leave_contract_id = value
        elif str(value).isdigit():  # Check if it's a numeric string
            leave_contract_id = int(value)
        else:
            raise serializers.ValidationError("Invalid leave_contract value.")

        try:
            leave_contract = LeaveContractModel.objects.get(id=leave_contract_id)
        except LeaveContractModel.DoesNotExist:
            raise serializers.ValidationError("Invalid leave_contract ID.")

        return leave_contract
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Fetch the related LeaveTypeModel object and serialize it
        default_leave_contract = instance.default_leave_contract
        if default_leave_contract:
            representation["default_leave_contract"] = LeaveContractSerializer(
                default_leave_contract
            ).data

        return representation

