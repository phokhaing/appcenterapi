from ..leave_reason.models import LeaveReasonModel
from rest_framework import serializers
from .models import LeaveRequest, LeaveRequestStatus
from ...user_management.serializer import UserListingSerializer
from ..leave_type.serializer import LeaveTypeSerializer
from django.contrib.auth import get_user_model
from ..leave_file.serializer import LeaveFileSerializer
from ..leave_balance.models import LeaveBalance
from app.utils.GlobalHelper import GlobalHelper
from app.utils.IdEncryption import IdEncryption
from app.user_management.serializer import UserAvatarSerializer
from app.user_management.models import UserAvatar

User = get_user_model()


class LeaveRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequestStatus
        fields = "__all__"


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = "__all__"


class LeaveRequestViewSerializer(serializers.ModelSerializer):
    requested_by = serializers.StringRelatedField(source="requested_by.fullname")
    certifier = serializers.StringRelatedField(source="certifier.fullname")
    certifier_by = serializers.StringRelatedField(source="certifier_by.fullname")
    authorizer = serializers.StringRelatedField(source="authorizer.fullname")
    authorizer_by = serializers.StringRelatedField(source="authorizer_by.fullname")
    rejected_by = serializers.StringRelatedField(source="rejected_by.fullname")
    canceled_by = serializers.StringRelatedField(source="canceled_by.fullname")
    created_by = serializers.StringRelatedField(source="created_by.fullname")
    leave_type = serializers.StringRelatedField(source="leave_type.name")
    staff_branch = serializers.SerializerMethodField()
    staff_gender = serializers.SerializerMethodField()
    leave_files = LeaveFileSerializer(many=True, source="leave_files.all")
    leave_status = LeaveRequestStatusSerializer(required=False)
    current_annual_leave_by_hour = serializers.SerializerMethodField()
    staff_avatar = serializers.SerializerMethodField()

    # requested_by = serializers.StringRelatedField(source='requested_by.fullname')
    # certifier = serializers.StringRelatedField(source='certifier.fullname')
    # certifier_by = serializers.StringRelatedField(source='certifier_by.fullname')
    # authorizer = serializers.StringRelatedField(source='authorizer.fullname')
    # authorizer_by = serializers.StringRelatedField(source='authorizer_by.fullname')
    # rejected_by = serializers.StringRelatedField(source='rejected_by.fullname')
    # created_by = serializers.StringRelatedField(source='created_by.fullname')
    # leave_type = serializers.StringRelatedField(source='leave_type.name')
    # staff_branch = serializers.SerializerMethodField()
    # staff_gender = serializers.SerializerMethodField()
    # leave_files = LeaveFileSerializer(many=True, source='leave_files.all')
    # leave_status = LeaveRequestStatusSerializer(required=False)
    # current_annual_leave_by_hour = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "user_id",
            "staff_id",
            "staff_name",
            "staff_position",
            "staff_department",
            "staff_branch",
            "staff_gender",
            "leave_status",
            "leave_status",
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
            "authorizer_by",
            "authorizer_at",
            "rejected_by",
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
            "leave_files",
            "current_annual_leave_by_hour",
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

    def get_staff_branch(self, obj):
        try:
            user_instance = obj.user_id
            user_info = GlobalHelper.find_user_info_by_user_id(user_instance.id)
            return user_info["branch"]
        except User.DoesNotExist:
            return None


class LeaveRequestListingSerializer(serializers.ModelSerializer):
    certifier = UserListingSerializer(required=False)
    certifier_by = UserListingSerializer(required=False)

    authorizer = UserListingSerializer(required=False)
    authorizer_by = UserListingSerializer(required=False)

    leave_type = LeaveTypeSerializer(required=False)

    staff_gender = serializers.SerializerMethodField()
    leave_files = LeaveFileSerializer(many=True, source="leave_files.all")
    leave_status = LeaveRequestStatusSerializer(required=False)

    total_time_by_hour = serializers.SerializerMethodField()
    encrypt_key = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = "__all__"

    def get_encrypt_key(self, instance):
        if not instance.id:
            return None
        return IdEncryption.encrypt_id(instance.id)

    def get_total_time_by_hour(self, instance):
        total_time = instance.total_time
        total_time_by_hour = total_time / 60
        return round(total_time_by_hour, 2)

    def get_staff_gender(self, obj):
        try:
            user_instance = obj.user_id
            return user_instance.gender
        except User.DoesNotExist:
            return None


class LeaveRequestFilterExportSerializer(serializers.ModelSerializer):
    certifier = serializers.StringRelatedField(source="certifier.fullname")
    certifier_by = serializers.StringRelatedField(source="certifier_by.fullname")
    certifier_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    authorizer = serializers.StringRelatedField(source="authorizer.fullname")
    authorizer_by = serializers.StringRelatedField(source="authorizer_by.fullname")
    authorizer_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    requested_by = serializers.StringRelatedField(source="requested_by.fullname")
    requested_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    rejected_by = serializers.StringRelatedField(source="rejected_by.fullname")
    rejected_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    canceled_by = serializers.StringRelatedField(source="canceled_by.fullname")
    canceled_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S", required=False)

    leave_type = serializers.StringRelatedField(
        source="leave_type.name", required=False
    )
    leave_status = serializers.StringRelatedField(
        source="leave_status.name", required=False
    )
    staff_gender = serializers.SerializerMethodField()
    staff_branch = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "user_id",
            "staff_id",
            "staff_name",
            "staff_gender",
            "staff_position",
            "staff_department",
            "staff_branch",
            "leave_type",
            "start_date",
            "end_date",
            "from_time",
            "to_time",
            "hours",
            "minute",
            "total_time",
            "reason",
            "leave_status",
            "requested_by",
            "requested_at",
            "certifier",
            "certifier_by",
            "certifier_at",
            "authorizer",
            "authorizer_by",
            "authorizer_at",
            "rejected_by",
            "rejected_at",
            "rejected_reason",
            "canceled_by",
            "canceled_at",
            "canceled_reason",
            "incharge_request",
            "incharge_certifier",
            "incharge_authorizer",
        ]

    def get_staff_gender(self, obj):
        try:
            user_instance = obj.user_id
            return user_instance.gender
        except User.DoesNotExist:
            return None

    def get_staff_branch(self, obj):
        try:
            user_instance = obj.user_id
            if user_instance:
                branch_instance = user_instance.branch
                if branch_instance:
                    return branch_instance.name_en
            return None
        except User.DoesNotExist:
            return None


class LeaveReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveReasonModel
        fields = "__all__"


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
