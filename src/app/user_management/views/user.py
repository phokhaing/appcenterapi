from django.http import Http404, HttpResponse
from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import viewsets, status, generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.core.paginator import Paginator

from .UserFilesView import UserFilesView
from ..filter import UserFilter
from ..models import (
    User,
    ModulePermission,
    RoleModule,
    UserRole,
    Module,
    Role,
    Permission,
    UserAvatar,
    GroupsUser,
    GroupMembership,
)
from ..serializer import (
    UserDetailsSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
    UpdateUserProfileSerializer,
    SuspendedUserSerializer,
    ResetPasswordSerializer,
    RoleSerializer,
    UserListingSerializer,
    CreateUserSerializer,
    UserFetchOneSerializer,
    GroupsUserSerializer,
    GroupMembershipSerializer,
    GroupMembershipViewSerializer,
    GroupsUserViewSerializer,
    GroupsUserListingSerializer,
    GroupMembershipListingSerializer,
)
from ..serializer.user import ForgotPasswordSerializer, UserAvatarSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.decorators import action
import pandas as pd
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponseForbidden
from decouple import config
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from ...utils.UserAccessPermission import permission_required
from django.conf import settings
from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse

from ...utils.EmailSending import send_email_inbound, getEmailTemplateByHook
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

# custom swagger
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ...utils.global_openapi_schema import (
    global_request_openapi_schema,
    global_response_openapi_shema,
)
from ...utils.FormDataToObject import convertToObject
from ...utils.UserAccessPermission import permission_api_view_required
from decouple import config
import datetime
import json
from django.http import HttpResponseForbidden
from django.db import transaction
import pytz

module_name = "SETTING/USER"

module_user_group = "SETTING/USER_GROUP"


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UserManagement(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    serializer_class = UserDetailsSerializer
    queryset = User.objects.all().order_by("-created_at")

    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = (
        "id",
        "staff_id",
        "username",
        "email",
        "first_name",
        "last_name",
        "first_name_kh",
        "last_name_kh",
        "gender",
        "phone_number",
        "ext",
        "is_active",
        # "branch",
        # "department",
        # "roles",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # search by field name
    filterset_class = UserFilter  # filter by field name

    def get_queryset(self):
        queryset = super().get_queryset()

        # Extract filters from the request
        branch_filter = self.request.query_params.get("branch_filter")
        department_filter = self.request.query_params.get("department_filter")
        role_filter = self.request.query_params.get("position_filter")
        position_filter = self.request.query_params.get("role_filter")
        is_active_filter = self.request.query_params.get("is_active_filter")

        # Apply filters if provided
        if branch_filter:
            queryset = queryset.filter(branch__id=branch_filter)

        if department_filter:
            queryset = queryset.filter(department__id=department_filter)

        if position_filter:
            queryset = queryset.filter(position__id=position_filter)

        if role_filter:
            queryset = queryset.filter(roles__id=role_filter)

        if is_active_filter:
            queryset = queryset.filter(is_active=is_active_filter)

        return queryset

    # for create

    # @permission_required(module_name, "CREATE")
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #
    #     # Assign the default role to the user
    #     default_role = get_object_or_404(Role, role_name_en="STAFF")
    #     UserRole.objects.create(user=serializer.instance, role=default_role)
    #
    #     return Response(
    #         serializer.data, status=status.HTTP_201_CREATED, headers=headers
    #     )

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            user_logged = request.user
            request_data = convertToObject(
                request.POST.dict(), "f->jk", "data_json")
            iso_date_str = request_data.get(
                "date_joined"
            )  # Assuming this is in ISO 8601 format
            # Convert ISO 8601 date to Python datetime object and specify the timezone as UTC
            iso_date = datetime.datetime.fromisoformat(
                iso_date_str.replace("Z", "+00:00")
            ).replace(tzinfo=pytz.UTC)
            # Convert the UTC datetime to Cambodian timezone (ICT - Indochina Time)
            cambodia_timezone = pytz.timezone("Asia/Phnom_Penh")
            local_date = iso_date.astimezone(cambodia_timezone)
            # Extract only the date part
            date_joined = local_date.date()
            context = {
                "staff_id": request_data.get("staff_id"),
                "first_name": request_data.get("first_name"),
                "last_name": request_data.get("last_name"),
                "first_name_kh": request_data.get("first_name_kh"),
                "last_name_kh": request_data.get("last_name_kh"),
                "email": request_data.get("email"),
                "gender": request_data.get("gender"),
                "address": request_data.get("address"),
                "phone_number": request_data.get("phone_number"),
                "ext": request_data.get("ext"),
                "pc_id": request_data.get("pc_id"),
                "ip_address": request_data.get("ip_address"),
                # 'date_joined': request_data.get('date_joined'),
                "date_joined": date_joined,
                "is_active": request_data.get("is_active"),
                "is_staff": request_data.get("is_staff"),
                "branch": request_data.get("branch"),
                "department": request_data.get("department"),
                "position": request_data.get("position"),
                "username": request_data.get("username"),
                "password": request_data.get("password"),
                "manager": request_data.get("manager"),
                "created_at": datetime.datetime.now(),
                "created_by": user_logged.id,
            }
            serializer = CreateUserSerializer(data=context)
            if serializer.is_valid():
                instance_user = serializer.save()

                # **** Assign default role STAFF ****#
                default_role = get_object_or_404(Role, role_name_en="STAFF")
                UserRole.objects.create(user=instance_user, role=default_role)

                # **** Save do upload file ****#
                files_view = UserFilesView()
                files_data = request.FILES.getlist("attachment_files") or []
                files_view.create_user_files(
                    files_data, user_logged, instance_user)

                response = {
                    "user data": serializer.data,
                }
                return Response(
                    {
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "message": "User has been created",
                        "data": response,
                    }
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            ValidationError({e})

    def perform_create(self, serializer):
        # serializer.save()
        serializer.save(created_by=self.request.user,
                        created_at=timezone.now())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user,
                        updated_at=timezone.now())

    # for update
    # def get_serializer_class(self):
    # 	if self.action == "create":
    # 		return CreateUserSerializer
    #
    # 	if self.action == "update":
    # 		return UpdateUserSerializer
    #
    # 	return super().get_serializer_class()

    @permission_required(module_name, "LIST")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_name, "UPDATE")
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        try:
            user_logged = request.user
            request_data = convertToObject(
                request.POST.dict(), "f->jk", "data_json")

            iso_date_str = request_data.get(
                "date_joined"
            )  # Assuming this is in ISO 8601 format
            # Convert ISO 8601 date to Python datetime object and specify the timezone as UTC
            iso_date = datetime.datetime.fromisoformat(
                iso_date_str.replace("Z", "+00:00")
            ).replace(tzinfo=pytz.UTC)
            # Convert the UTC datetime to Cambodian timezone (ICT - Indochina Time)
            cambodia_timezone = pytz.timezone("Asia/Phnom_Penh")
            local_date = iso_date.astimezone(cambodia_timezone)
            # Extract only the date part
            date_joined = local_date.date()

            instance = self.get_object()
            context_update = {
                "staff_id": request_data.get("staff_id"),
                "first_name": request_data.get("first_name"),
                "last_name": request_data.get("last_name"),
                "first_name_kh": request_data.get("first_name_kh"),
                "last_name_kh": request_data.get("last_name_kh"),
                "email": request_data.get("email"),
                "gender": request_data.get("gender"),
                "address": request_data.get("address"),
                "phone_number": request_data.get("phone_number"),
                "ext": request_data.get("ext"),
                "pc_id": request_data.get("pc_id"),
                "ip_address": request_data.get("ip_address"),
                "date_joined": date_joined,
                # 'date_joined': request_data.get('date_joined'),
                "is_active": request_data.get("is_active"),
                "is_staff": request_data.get("is_staff"),
                "branch": request_data.get("branch"),
                "department": request_data.get("department"),
                "position": request_data.get("position"),
                "manager": request_data.get("manager"),
                "updated_at": datetime.datetime.now(),
                "updated_by": user_logged.id,
                "username": request_data.get("username"),
            }
            serializer = UpdateUserSerializer(
                instance, data=context_update, partial=True
            )
            if serializer.is_valid():
                serializer.save()

                # Update file upload
                files_view = UserFilesView()
                file_data = request_data.get("attachment_files", [])
                files_new_upload = request.FILES.getlist("attachment_files")
                files_res = files_view.update_user_files(
                    file_data, files_new_upload, user_logged, instance
                )

                response = {
                    "purchase_data": serializer.data,
                    "attachment_files": files_res,
                }

                return Response(
                    {
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "message": "User has been updated",
                        "data": response,
                    }
                )
            else:
                # Handle invalid serializer data
                return Response(
                    {
                        "success": False,
                        "status": status.HTTP_400_BAD_REQUEST,
                        "message": "Invalid data",
                        "errors": serializer.errors,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Validation error",
                    "errors": str(e),  # Convert ValidationError to string
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    @permission_required(module_name, "VIEW")
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = UserFetchOneSerializer(
                instance)  # Using custom serializer
            return Response(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "data": serializer.data,
                }
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Cannot retrieve the instance."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @permission_required(module_name, "DELETE")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


# method generated token data
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        if user is not None:
            user_position = model_to_dict(
                user.position) if user.position else None
            user_department = (
                model_to_dict(user.department) if user.department else None
            )
            user_branch = model_to_dict(user.branch) if user.branch else None

            # default avatar path is  file_storage/profile1.png
            # avatar_url = (
            # 	settings.GET_MEDIA_URL + "/" + str(user.photo)
            # 	if user.photo
            # 	else settings.GET_MEDIA_URL + "/profile1.png"
            # )

            avatar_url = None
            # Retrieve avatar URL using UserAvatarSerializer
            try:
                user_avatar = UserAvatar.objects.get(user_id=user.id)
                avatar_url = f"{settings.GET_MEDIA_URL}/{user_avatar.file_path}/{user_avatar.upload_file_name}"
            except UserAvatar.DoesNotExist:
                pass

            manager_staff = None
            if user.manager:
                manager_staff = user.manager.fullname

            date_joined = user.date_joined
            date_joined_formatted_date = date_joined.strftime("%B %d, %Y")

            # Add custom claims
            token["data"] = {
                "staff_id": user.staff_id,
                "user_id": user.id,
                "username": user.username,
                "fullname": user.fullname,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "first_name_kh": user.first_name_kh,
                "last_name_kh": user.last_name_kh,
                "email": user.email,
                "gender": user.gender,
                "avatar": avatar_url,
                "address": user.address,
                "phone_number": user.phone_number,
                "manager": manager_staff,
                "is_active": user.is_active,
                "date_joined": date_joined_formatted_date,
                "user_position": user_position["name_en"] if user_position else None,
                "user_department": (
                    user_department["name_en"] if user_department else None
                ),
                "user_branch": user_branch["name_en"] if user_branch else None,
                "branch_id": user_branch["id"] if user_branch else None,
            }
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# class UserLogout(APIView):
#    authentication_classes = [TokenAuthentication]
#    # permission_classes = [IsAuthenticated]
#
#    def get(self, request):
#       request.user.auth_token.delete()
#       return Response({
#          'status': status.HTTP_200_OK,
#          'message': 'User logged out successfully',
#       })


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserProfileSerializer


class SuspendedUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SuspendedUserSerializer

    @permission_required(module_name, "SUSPENDED_USER")
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data={"is_active": False, "is_staff": False}, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User suspended updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})


class ResetPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordSerializer

    @permission_required(module_name, "RESET_PASSWORD")
    def update(self, request, *args, **kwargs):
        # Call the superclass's update() method to perform the update
        response = super().update(request, *args, **kwargs)

        # Create a custom response message and status code
        message = "Password reset successfully"
        status_code = status.HTTP_200_OK

        # Update the response with the custom message and status code
        response.data = {"message": message}
        response.status_code = status_code

        return response


class UserPermissionsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        module_name = request.GET.get("module_name")

        user = request.user
        if not user:
            # User not found, deny access
            return HttpResponseForbidden("User not found")

        user_roles = user.roles.all()
        if not user_roles:
            # User has no roles, deny access
            return HttpResponseForbidden("User has no roles")

        module = Module.objects.filter(module_name=module_name).first()
        if not module:
            # Module not found, deny access
            return HttpResponseForbidden("Module not found")

        # Retrieve the module permissions for the user's roles
        permissions = ModulePermission.objects.filter(
            module=module,
            role__in=user_roles,
        ).values_list("permission__permission_name", flat=True)

        # Convert the permissions queryset to a list of permission names
        permission_names = list(permissions)

        # Return the permission names as JSON response
        return JsonResponse({"moduleName": module_name, "permission": permission_names})


class ListRoleByUserIDAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user_roles = user.roles.all()

            role_ids = user_roles.values_list("id", flat=True)
            roles = Role.objects.filter(id__in=role_ids)

            data = []
            for role in roles:
                role_data = {
                    "id": UserRole.objects.get(user=user, role=role).id,
                    "role_id": role.id,
                    "role_name": role.role_name_en,
                    "user_id": user_id,
                }
                data.append(role_data)

            return Response(data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class ListRoleNotExistingByUserIDAPIView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            roles = Role.objects.exclude(users=user)
            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response(
                {"message": "Role not found."}, status=status.HTTP_404_NOT_FOUND
            )


class UpdateUserRoleAPIView(APIView):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        roles = request.data.get("roles", [])
        # Update the user roles
        role_ids = [role["value"] for role in roles]  # Extract the role IDs

        # Update the user roles
        user.roles.set(role_ids)

        # Insert new roles
        for role_id in role_ids:
            if not user.roles.filter(id=role_id).exists():
                user.roles.add(role_id)

        return Response(
            {"success": True, "message": "User roles updated successfully."}
        )


class UserListing(APIView):
    def get(self, request):
        # queryset = User.objects.all()
        queryset = User.objects.filter(is_active=1)
        serializer = UserListingSerializer(queryset, many=True)
        return Response(serializer.data)


class UserListingPagination(APIView):
    def get(self, request):
        fields = (
            "id",
            "staff_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "first_name_kh",
            "last_name_kh",
            "gender",
            "phone_number",
        )
        search_fields = fields
        filter_fields = fields

        queryset = User.objects.all()

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=UserListingSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="user listing with pagination retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )


# ------------------------------------------------------------
# @author: Pho Khaing
# @date  : 16-11-2023
# @method: Account fonfirmation & Password Recovery
# After submitted, Link reset password will send to your email
# ------------------------------------------------------------
# @param required:
# content data: {"username": string, "email": string}
# ------------------------------------------------------------
class ForgotPasswordView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Account Confirmation & Password Recovery",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=["username", "email"],
        ),
        responses={
            200: "Success will send link reset password to your email account.",
            400: "Bad request response description",
        },
    )
    def post(self, request):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            if serializer.is_valid():
                username = serializer.validated_data["username"]
                email = serializer.validated_data["email"]

                user = User.objects.get(username=username, email=email)

                # Generate password reset token
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # create reset link
                reset_link = (
                    f"{settings.DOMAIN_WEB}/reset_password?token={access_token}"
                )
                send_confirmation_email(username, email, reset_link)

                context = {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Confirmation email sent. please check your email address.",
                    "data": {"resetLink": reset_link},
                }

                return Response(context, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            context = {
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid username or email.",
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------
# @author: Pho Khaing
# @date  : 16-11-2023
# @method: this method for user who forgot password, they can change
# own account password without signin
# ----------------------------------------------------------------
# @param required:
# url param: ?userid=int
# content data: {"password": string, "password2": string}
# ----------------------------------------------------------------
@swagger_auto_schema(
    method="PUT",
    operation_description="Set new password for your account",
    manual_parameters=[
        openapi.Parameter(
            name="userid",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="User ID",
            required=True,
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "password2": openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=["password", "password2"],
    ),
    responses=global_response_openapi_shema(ResetPasswordSerializer),
)
@api_view(["PUT"])
@permission_classes([AllowAny])
def set_new_password(request):
    try:
        userid = request.GET.get("userid", None)
        user = User.objects.get(id=userid)
        serializer = ResetPasswordSerializer(instance=user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            context = {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "Your password has been changed.",
                "data": {
                    userid: userid,
                },
            }
            return Response(context, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        context = {
            "success": False,
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "User not found!",
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------------------------
# @author: Pho Khaing
# @date  : 15-11-2023
# @detail: Send email confirmation of password recovery
# -------------------------------------------------------------------
def send_confirmation_email(username, email, link_url):
    email_template = getEmailTemplateByHook("PASSWORD_RECOVERY")
    if not email_template:
        return Response(
            {"error": "Invalid email template hook PASSWORD_RECOVERY"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.filter(username=username).get()
    gender = ""
    to_user = "Sir/Madam"
    to_email = email

    if user:
        to_user = user.fullname
        to_email = user.email
        if user.gender == "M":
            gender = "Mr. "
        elif user.gender == "F":
            gender = "Mrs. "

    email_title = email_template.title
    email_body = email_template.message
    message_body = {
        "[TO_USER]": f"{gender}{to_user}",
        "[SITE_URL]": link_url,
        "[SITE_NAME]": settings.SITE_NAME,
    }
    email_content = email_body
    # Replace the keywords in the user-specific message
    for keyword, replacement in message_body.items():
        email_content = email_content.replace(keyword, replacement)
    # send email inbound configuration
    send_email_inbound(email_title, email_content, to_email)


class UserPermissionsApprovalLog(APIView):
    def get(self, request, *args, **kwargs):
        module_name = request.GET.get("module_name")
        permission_name = request.GET.get("permission_name")

        user = request.user
        if not user:
            return HttpResponseForbidden("User not found")

        module = Module.objects.filter(module_name=module_name).first()
        permission = Permission.objects.filter(
            permission_name=permission_name).first()

        if not module or not permission:
            return HttpResponseForbidden("Module or Permission not found")

        # Retrieve roles associated with the user within the specified module
        user_roles_in_module = user.roles.filter(modules=module)

        # Check if any of the user's roles have the required permission within the module
        user_has_permission = False
        for role in user_roles_in_module:
            if ModulePermission.objects.filter(
                role=role, module=module, permission=permission
            ).exists():
                user_has_permission = True
                break

        if not user_has_permission:
            response = {"message": "success", "data": 0}
            return Response(data=response, status=status.HTTP_200_OK)

        response = {"message": "success", "data": 1}
        return Response(data=response, status=status.HTTP_200_OK)


class GroupUserController:

    # *-----------------------------------------------------------------* #
    # *--------------------- list user by group id ---------------------* #
    # *-----------------------------------------------------------------* #
    @api_view(["GET"])
    @transaction.atomic
    def existing_user_listing(request, group_id):
        existing_user = GroupMembership.objects.filter(
            group_id=group_id).values_list("user_id", flat=True)

        user_ids = list(existing_user)

        queryset = User.objects.filter(is_active=1).exclude(id__in=user_ids)

        serializer = UserListingSerializer(queryset, many=True)

        return Response(serializer.data)

    # *-----------------------------------------------------------------* #
    # *----- list data by pagination, filter, search of group user -----* #
    # *-----------------------------------------------------------------* #
    @swagger_auto_schema(
        method="GET",
        operation_description="Retrieve a list of group user with pagination, search, and filtering",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Page number",
                required=False,
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of items per page",
                required=False,
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Search data",
                required=False,
            ),
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by ID",
                required=False,
            ),
            openapi.Parameter(
                name="title",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by title",
                required=False,
            ),
            openapi.Parameter(
                name="hook",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by hook",
                required=False,
            ),
        ],
    )
    @api_view(["GET"])
    @permission_api_view_required(module_user_group, "LIST")
    @transaction.atomic
    def list_group_user(request):

        search_fields = ["id", "title", "hook"]
        filter_fields = ["id", "title", "hook", "created_by", "created_at"]

        queryset = GroupsUser.objects.order_by("-created_at")

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=GroupsUserListingSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="Groups user list retrieved successfully.",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    # *-----------------------------------------------------------------* #
    # *----- list data by pagination, filter, search of membership -----* #
    # *-----------------------------------------------------------------* #
    @swagger_auto_schema(
        method="GET",
        operation_description="Retrieve a list of group user with pagination, search, and filtering",
        manual_parameters=[
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Page number",
                required=False,
            ),
            openapi.Parameter(
                name="page_size",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Number of items per page",
                required=False,
            ),
            openapi.Parameter(
                name="search",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Search data",
                required=False,
            ),
        ],
    )
    @api_view(["GET"])
    @transaction.atomic
    def list_membership(request, group_id):

        search = request.GET.get("search")
        page_size = int(request.GET.get("page_size", 10))
        page_number = int(request.GET.get("page", 1))

        queryset = GroupMembership.objects.filter(
            group_id=group_id
        ).order_by("-created_at")

        # Custom filter for searching by user_id__fullname
        if search:
            queryset = queryset.filter(
                Q(user_id__first_name__icontains=search) |
                Q(user_id__last_name__icontains=search)
            )

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = GroupMembershipListingSerializer(page_obj, many=True)

        return Response({
            "results": serializer.data,
            "count": paginator.count,
            "page": page_obj.number,
            "pages": paginator.num_pages,
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous_page": page_obj.previous_page_number() if page_obj.has_previous() else None,
        })

    # *-----------------------------------------------------------------* #
    # *------------------------ VIEW GROUP USER ------------------------* #
    # *-----------------------------------------------------------------* #

    @api_view(["GET"])
    @permission_api_view_required(module_user_group, "VIEW")
    def view_group_user(request, id):
        try:
            queryset = GroupsUser.objects.get(id=id)
            serializer = GroupsUserViewSerializer(queryset)

            return ApiResponse.success(
                message="Groups user retrieved successfully.",
                results=serializer.data,
            )
        except GroupsUser.DoesNotExist:
            return ApiResponse.not_found()

    # *-----------------------------------------------------------------* #
    # *----------------------- CREATE GROUP USER -----------------------* #
    # *-----------------------------------------------------------------* #
    @swagger_auto_schema(
        method="POST",
        operation_description="Create a new groups user",
        request_body=global_request_openapi_schema(GroupsUserSerializer),
        responses=global_response_openapi_shema(GroupsUserSerializer),
    )
    @api_view(["POST"])
    @permission_api_view_required(module_user_group, "CREATE")
    def create_group_user(request):
        try:
            # Assign the user to the request data
            request.data['created_by'] = request.user.id
            # Create a serializer instance with request data
            serializer = GroupsUserSerializer(data=request.data)
            # Validate the serializer data
            if serializer.is_valid():
                # Save the serializer data
                serializer.save()
                # Return a success response
                return ApiResponse.success(
                    message="Groups user created successfully.",
                    results=serializer.data,
                )
            else:
                # Return an error response if serializer data is not valid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # except PurchaseSettingModel.error:
        except Exception as e:
            # Return error response if an exception occurs
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e)
                }
            )

    # *-----------------------------------------------------------------* #
    # *----------------------- UPDATE GROUP USER -----------------------* #
    # *-----------------------------------------------------------------* #
    @swagger_auto_schema(
        method="PUT",
        operation_description="Update group user",
        request_body=global_request_openapi_schema(GroupsUserSerializer),
        responses=global_response_openapi_shema(GroupsUserSerializer),
    )
    @api_view(["PUT"])
    @permission_api_view_required(module_user_group, "UPDATE")
    def update_group_user(request, id):
        user_log = request.user
        try:
            instance = GroupsUser.objects.get(pk=id)
        except GroupsUser.DoesNotExist:
            return ApiResponse.not_found()

        try:
            serializer = GroupsUserSerializer(instance, data=request.data)

            if serializer.is_valid():
                serializer.validated_data["updated_by"] = user_log
                serializer.validated_data["updated_at"] = timezone.now()
                serializer.save()
                return ApiResponse.success(
                    message="Group user updated successfully.",
                    results=serializer.data,
                )
            else:
                return ApiResponse.error(errors=serializer.errors)
        except Exception as e:
            return ApiResponse.error(message=str(e))

    # *-----------------------------------------------------------------* #
    # *-------------------- CREATE GROUP MEMBERSHIP --------------------* #
    # *-----------------------------------------------------------------* #
    @swagger_auto_schema(
        method="POST",
        operation_description="Create a new group membership",
        request_body=global_request_openapi_schema(GroupMembershipSerializer),
        responses=global_response_openapi_shema(GroupMembershipSerializer),
    )
    @api_view(["POST"])
    @permission_api_view_required(module_user_group, "CREATE")
    def create_group_membership(request):
        user_log = request.user.id
        try:
            group_id = request.data.get("group_id")
            user_ids = request.data.get("user_id", [])

            for user_id in user_ids:
                context = {
                    "group_id": group_id,
                    "user_id": user_id,
                    "created_by": user_log,
                    "created_at": timezone.now(),
                }

                serializer = GroupMembershipSerializer(data=context)

                if serializer.is_valid():
                    serializer.save()
                else:
                    errors = serializer.errors
                    return Response(
                        {
                            "success": False,
                            "status": status.HTTP_400_BAD_REQUEST,
                            "message": "Validation error",
                            "errors": errors
                        }
                    )

            return Response(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Group membership created successfully.",
                }
            )

        except Exception as e:
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": str(e)
                }
            )

    # *-----------------------------------------------------------------* #
    # *-------------------- DELETE MEMBERSHIP GROUP --------------------* #
    # *-----------------------------------------------------------------* #

    @api_view(["DELETE"])
    @permission_api_view_required(module_user_group, "DELETE")
    def delete_group_user(request, id):
        try:
            queryset = GroupsUser.objects.get(pk=id)
            queryset.delete()
            return ApiResponse.success(
                message="Group user deleted successfully.",
            )
        except GroupsUser.DoesNotExist:
            return ApiResponse.not_found()

    # *-----------------------------------------------------------------* #
    # *----------------------- DELETE GROUP USER -----------------------* #
    # *-----------------------------------------------------------------* #
    @api_view(["DELETE"])
    @permission_api_view_required(module_user_group, "DELETE")
    def delete_user_membership(request, id):
        try:
            membership = GroupMembership.objects.get(id=id)
        except GroupMembership.DoesNotExist:
            return ApiResponse.not_found(message="Group membership not found.")

        try:
            membership.delete()
            return ApiResponse.success(message="Group membership deleted successfully.")
        except Exception as e:
            return ApiResponse.error(message=str(e))
