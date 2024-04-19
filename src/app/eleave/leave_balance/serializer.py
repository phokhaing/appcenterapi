from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import LeaveBalance

User = get_user_model()


class LeaveBalanceSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source="created_by.fullname")
    updated_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )
    user_id = serializers.StringRelatedField(source="employee.username")
    user_fullname = serializers.StringRelatedField(source="employee.fullname")
    staff_id = serializers.StringRelatedField(source="employee.staff_id")
    staff_dept = serializers.StringRelatedField(source="employee.department")
    staff_branch = serializers.StringRelatedField(source="employee.branch")

    class Meta:
        model = LeaveBalance
        fields = "__all__"


class LeaveBalanceFetchOneSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(source="created_by.fullname")
    updated_by = serializers.StringRelatedField(source="updated_by.fullname")
    user_id = serializers.StringRelatedField(source="employee.username")
    user_fullname = serializers.StringRelatedField(source="employee.fullname")
    staff_id = serializers.StringRelatedField(source="employee.staff_id")
    staff_dept = serializers.StringRelatedField(source="employee.department")
    staff_branch = serializers.StringRelatedField(source="employee.branch")

    created_at = serializers.DateTimeField(format="%d/%b/%Y %I:%M %p")
    updated_at = serializers.DateTimeField(format="%d/%b/%Y %I:%M %p")

    class Meta:
        model = LeaveBalance
        fields = "__all__"
