from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import Serializer

from ..models import User, UserAvatar, UserRole, GroupsUser, GroupMembership
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from app.utils.GlobalHelper import GlobalHelper


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    address = serializers.CharField(required=False, write_only=True)

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    # def custom_signup(self, request, user):
    #     pass

    def get_cleaned_data(self):
        return {
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "address": self.validated_data.get("address", ""),
            "user_type": self.validated_data.get("user_type", ""),
            "password1": self.validated_data.get("password1", ""),
            "email": self.validated_data.get("email", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        user.save()
        return user


class UserAvatarSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, instance):
        base_url = settings.GET_MEDIA_URL
        return f"{base_url}/images/profile/{instance.upload_file_name}"

    class Meta:
        model = UserAvatar
        fields = "__all__"


class UserDetailsSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Convert 'updated_by' to username
        created_by = instance.created_by
        updated_by = instance.updated_by
        manager = instance.manager

        if created_by is not None:
            representation["created_by"] = created_by.username

        if updated_by is not None:
            representation["updated_by"] = updated_by.username

        if manager is not None:
            representation["manager"] = {
                "id": manager.id, "username": manager.username}

        return representation

    created_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", required=False)
    updated_at = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", required=False)

    # date_joined = serializers.DateTimeField(format="%m/%d/%Y")

    avatar = UserAvatarSerializer(many=True, source="attachment_files.all")

    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "email",
            "gender",
            "address",
            "phone_number",
            "ext",
            "pc_id",
            "ip_address",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "branch",
            "department",
            "position",
            "roles",
            "username",
            "password",
            # "photo",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "manager",
            "avatar",
        )
        # read_only_fields = ("email", "password")
        read_only_fields = (
            "is_superuser",
            "roles",
        )
        depth = 1


class CreateUserSerializer(serializers.ModelSerializer):
    def validate_staff_id(self, value):
        if User.objects.filter(staff_id=value).exists():
            raise serializers.ValidationError("This staff ID already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    @staticmethod
    def validate_password(password: str) -> str:
        return make_password(password)

    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "email",
            "gender",
            "address",
            "phone_number",
            "ext",
            "pc_id",
            "ip_address",
            "date_joined",
            "is_active",
            "is_staff",
            "branch",
            "department",
            "position",
            "username",
            "password",
            "manager",
            "created_at",
            "created_by",
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("old_password", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data["password"])
        instance.save()

        return instance


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def validate_username(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]

        instance.save()
        return instance


class UpdateUserSerializer(serializers.ModelSerializer):

    def validate_staff_id(self, value):
        instance = self.instance  # Getting the current instance being updated
        if instance and instance.staff_id == value:
            return value  # No change in staff_id, so validation passed

        queryset = (
            User.objects.exclude(
                pk=instance.pk) if instance else User.objects.all()
        )
        if queryset.filter(staff_id=value).exists():
            raise serializers.ValidationError("Staff ID already taken.")
        return value

    def validate_email(self, value):
        instance = self.instance  # Getting the current instance being updated
        if instance and instance.email == value:
            return value  # No change in email, so validation passed

        queryset = (
            User.objects.exclude(
                pk=instance.pk) if instance else User.objects.all()
        )
        if queryset.filter(email=value).exists():
            raise serializers.ValidationError("Email already taken.")
        return value

    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "email",
            "gender",
            "address",
            "phone_number",
            "ext",
            "pc_id",
            "ip_address",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "branch",
            "department",
            "position",
            "photo",
            "created_by",
            "created_at",
            "updated_by",
            "updated_at",
            "manager",
            "username",
        )


class SuspendedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "is_active",
            "is_staff",
        )


class ResetPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "staff_id",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "username",
            "email",
            "fullname",
            "position",
        )


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class UserFetchOneSerializer(serializers.ModelSerializer):
    attachment_files = UserAvatarSerializer(
        many=True, source="attachment_files.all")
    created_by_str = serializers.StringRelatedField(
        source="created_by.fullname")
    updated_by_str = serializers.StringRelatedField(
        source="updated_by.fullname")
    created_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")

    class Meta:
        model = User
        fields = "__all__"


class GroupsUserListingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')

    class Meta:
        model = GroupsUser
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = {
                "id": created_by.id,
                "fullname": created_by.fullname
            }

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = {
                "id": updated_by.id,
                "fullname": updated_by.fullname
            }

        return representation


class GroupsUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupsUser
        fields = "__all__"

    def create(self, validated_data):
        # Modify validated_data before creating the instance
        hook = validated_data.get('hook', '')
        validated_data['hook'] = hook.upper().replace(' ', '_')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Modify validated_data before updating the instance
        hook = validated_data.get('hook', '')
        validated_data['hook'] = hook.upper().replace(' ', '_')

        return super().update(instance, validated_data)

    # def validate_hook(self, value):

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = {
                "id": created_by.id,
                "fullname": created_by.fullname
            }

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = {
                "id": updated_by.id,
                "fullname": updated_by.fullname
            }

        return representation


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = "__all__"


class GroupMembershipListingSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')
    title = serializers.SerializerMethodField()

    class Meta:
        model = GroupMembership
        fields = "__all__"

    def get_title(self, obj):
        try:
            group_id = obj.group_id.id
            group = GroupsUser.objects.get(id=group_id)
            return group.title
        except GroupsUser.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        user = instance.user_id
        if user:
            representation["user_id"] = user.fullname

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = created_by.fullname

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = created_by.fullname

        return representation


class GroupMembershipViewSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')

    class Meta:
        model = GroupMembership
        fields = [
            'id',
            'group_id',
            'user_id',
            'user_fullname',
            'status',
            'created_by',
            'created_at',
            'updated_by',
            'updated_at'
        ]

    def get_user_fullname(self, obj):
        try:
            user_id = obj.user_id.id
            user_fullname = GlobalHelper.show_user_fullname_en(user_id)
            return user_fullname
        except User.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = {
                "id": created_by.id,
                "fullname": created_by.fullname
            }

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = {
                "id": updated_by.id,
                "fullname": updated_by.fullname
            }

        return representation


class GroupsUserViewSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')
    updated_at = serializers.DateTimeField(format='%d/%m/%Y, %I:%M:%S %p')

    class Meta:
        model = GroupsUser
        fields = [
            'id',
            'title',
            'hook',
            'users',
            'status',
            'created_by',
            'created_at',
            'updated_by',
            'updated_at'
        ]

    def get_users(self, obj):
        try:
            all_users = GroupMembership.objects.filter(
                group_id=obj.id
            )
            serializer = GroupMembershipViewSerializer(
                all_users, many=True
            )
            return serializer.data
        except GroupMembership.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        created_by = instance.created_by
        if created_by:
            representation["created_by"] = created_by.fullname
            # {
            #     # "id": created_by.id,
            #     "fullname": created_by.fullname
            # }

        updated_by = instance.updated_by
        if updated_by:
            representation["updated_by"] = updated_by.fullname
            # {
            #     # "id": updated_by.id,
            #     "fullname": updated_by.fullname
            # }

        return representation
