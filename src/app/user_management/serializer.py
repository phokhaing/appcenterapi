from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.conf import settings
from rest_framework import serializers

from .models import User


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
            raise serializers.ValidationError(("The two password fields didn't match."))
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
        return user

        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        # fields = '__all__'
        fields = (
            "pk",
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
            "is_active",
            "is_staff",
            "is_superuser",
            "branch",
            "department",
            "position",
        )
        read_only_fields = ("email", "password")
        depth = 1
