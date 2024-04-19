#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : SOY DARA                                       |
#  | EMAIL: soydara168@gmail.com                           |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from rest_framework import serializers
from ..leave_request.models import LeaveRequest, LeaveRequestStatus
from ..leave_type.models import LeaveTypeModel
from ..leave_balance.models import LeaveBalance
from django.contrib.auth import get_user_model
from ..leave_file.serializer import LeaveFileSerializer
from app.utils.IdEncryption import IdEncryption
from app.utils.GlobalHelper import GlobalHelper

User = get_user_model()


class LeaveBalanceSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = "__all__"


class UserGenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["staff_id"]


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["fullname"]


class LeaveTypeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveTypeModel
        fields = ["name"]


class LeaveRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestStatus
        fields = ["id", "name"]


class LeaveRequestSummarySerializer(serializers.ModelSerializer):
    encrypt_key = serializers.SerializerMethodField()
    requested_by = serializers.StringRelatedField(source="requested_by.fullname")
    certifier = serializers.StringRelatedField(source="certifier.fullname")
    certifier_by = serializers.StringRelatedField(source="certifier_by.fullname")
    authorizer = serializers.StringRelatedField(source="authorizer.fullname")
    authorizer_by = serializers.StringRelatedField(source="authorizer_by.fullname")
    rejected_by = serializers.StringRelatedField(source="rejected_by.fullname")
    created_by = serializers.StringRelatedField(source="created_by.fullname")
    leave_type = serializers.StringRelatedField(source="leave_type.name")
    staff_gender = serializers.SerializerMethodField()
    leave_files = LeaveFileSerializer(many=True, source="leave_files.all")
    # leave_status = LeaveRequestStatusSerializer(required=False)
    leave_status = serializers.StringRelatedField(source="leave_status.name")
    current_annual_leave_by_hour = serializers.SerializerMethodField()
    staff_avatar = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "user_id",
            "staff_id",
            "staff_name",
            "staff_position",
            "staff_department",
            "staff_gender",
            "start_date",
            "end_date",
            "from_time",
            "to_time",
            "hours",
            "minute",
            "total_time",
            "reason",
            "requested_at",
            "requested_by",
            "certifier",
            "certifier_by",
            "certifier_at",
            "authorizer",
            "authorizer_by",  #
            "authorizer_at",
            "rejected_by",  #
            "rejected_reason",
            "rejected_at",
            "canceled_by",
            "canceled_reason",
            "canceled_at",
            "incharge_request",
            "incharge_certifier",
            "incharge_authorizer",
            "leave_type",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "leave_status",
            "leave_files",
            "current_annual_leave_by_hour",
            "encrypt_key",
            "staff_avatar",
        ]

    def get_staff_avatar(self, obj):
        try:
            user_instance = obj.user_id
            user_avatar = GlobalHelper.find_user_avatar_by_user_id(user_instance.id)

            return user_avatar
        except User.DoesNotExist:
            return None

    def get_current_annual_leave_by_hour(self, obj):
        try:
            user_instance = obj.user_id
            queryset = (
                LeaveBalance.objects.filter(employee=user_instance)
                .order_by("-year")
                .first()
            )
            if queryset is not None:
                current_annual_leave = queryset.current_annual_leave / 60
                return round(current_annual_leave, 2)
            else:
                return None
        except LeaveBalance.DoesNotExist:
            return None

    def get_staff_gender(self, obj):
        try:
            user_instance = (
                obj.user_id
            )  # Assuming user_id is a ForeignKey to User model
            return user_instance.gender
        except User.DoesNotExist:
            return None

    def get_encrypt_key(self, instance):
        if not instance.id:
            return None
        return IdEncryption.encrypt_id(instance.id)


class LeaveRequestCertifierSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["certifier_by", "certifier_at", "leave_status"]


class LeaveRequestApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["authorizer_by", "authorizer_at", "leave_status"]


class LeaveRequestRejectSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["rejected_by", "rejected_at", "rejected_reason", "leave_status"]


class LeaveRequestCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ["canceled_by", "canceled_at", "canceled_reason", "leave_status"]


class CustomPaginationSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    page = serializers.IntegerField()
    pages = serializers.IntegerField()
    page_size = serializers.IntegerField()
    next_page = serializers.IntegerField(allow_null=True)
    next_page_url = serializers.URLField(allow_null=True)
    previous_page = serializers.IntegerField(allow_null=True)
    previous_page_url = serializers.URLField(allow_null=True)
