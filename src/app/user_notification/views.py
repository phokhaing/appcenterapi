#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : Soy Dara                                     |
#  | EMAIL: soydara168@gmail.com                       |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filter import (
    EmailHookFilter,
    EmailLanguageFilter,
    EmailTemplateFilter,
    NotificationFilter,
    UserOptionSelectFilter,
)
from .serializer import (
    EmailHookSerializer,
    EmailLanguageSerializer,
    EmailTemplateSerializer,
    NotificationSerializer,
    UserSerializer,
    UserListingNotiSerializer,
)
from .models import Notification, EmailHook, EmailLanguage, EmailTemplate

from django.conf import settings
from rest_framework import generics
from django.utils import timezone
from django.db.models import F
from rest_framework import status
from rest_framework.exceptions import ParseError
from ..utils.EmailSending import (
    send_email_inbound,
    send_email_outbound,
    getEmailTemplateByHook,
)
from ..utils import NotificationSending
from django.contrib.auth import get_user_model
from ..utils.GlobalHelper import GlobalHelper
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

User = get_user_model()


class EmailAPIView(APIView):
    def post(self, request):
        data = [
            {
                "user_id": 832,
                "user_first_name": "John",
                "user_last_name": "Smith",
                "email": "dara.soy@ftb.com.kh",
            },
            {
                "user_id": 598,
                "user_first_name": "Sambath",
                "user_last_name": "Christ",
                "email": "soydara168@gmail.com",
            },
        ]

        user_logged = request.user  # get logged request by user

        email_template = getEmailTemplateByHook("ASSESSMENT_LOAN")

        if email_template:
            template_title = email_template.title
            template_message = email_template.message

            for user in data:
                message_body = {
                    "[NAME]": user["user_first_name"] + " " + user["user_last_name"],
                    "[FIRST_NAME]": user_logged.first_name,
                    "[LAST_NAME]": user_logged.last_name,
                    "[SITE_URL]": settings.DOMAIN_NAME + "/my-site/loan/test/email",
                    "[SITE_NAME]": settings.SITE_NAME,
                    "[STATUS]": "Progress",
                    "[CODE]": "COD-0001",
                }
                # print("message_body:", message_body)
                # Create a copy of the template message
                user_template_message = template_message
                # Print the template message for debugging
                # print("template_message:", user_template_message)
                # Replace the keywords in the user-specific message
                for keyword, replacement in message_body.items():
                    user_template_message = user_template_message.replace(
                        keyword, replacement
                    )
                send_email_inbound(template_title, user_template_message, user["email"])
        else:
            return Response({"message": "Error email hook not found!"})


module_EmailHook = "EMAIL_SETTING/EMAIL_HOOK"


class EmailHookPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class EmailHookView(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = EmailHook.objects.all()
    serializer_class = EmailHookSerializer
    pagination_class = EmailHookPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = (
        "id",
        "hook",
        "hook_name",
        "status",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = [
        "hook",
        "hook_name",
    ]  # search by field name
    filterset_class = EmailHookFilter

    def perform_create(self, serializer):
        print(self.request)
        serializer.save(created_by=self.request.user, created_at=timezone.now())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())


module_EmailLanguage = "EMAIL_SETTING/EMAIL_LANGUAGE"


class EmailLanguagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class EmailLanguageView(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = EmailLanguage.objects.all()
    serializer_class = EmailLanguageSerializer
    pagination_class = EmailLanguagePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = (
        "id",
        "title",
        "status",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = [
        "title",
    ]  # search by field name
    filterset_class = EmailLanguageFilter

    def perform_create(self, serializer):
        # print(self.request)
        serializer.save(created_by=self.request.user, created_at=timezone.now())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())


module_EmailTemplate = "EMAIL_SETTING/EMAIL_TEMPLATE"


class EmailTemplatePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class EmailTemplateView(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    # filter_backends = (DjangoFilterBackend)

    fields = (
        "id",
        "title",
        "message",
        "hook",
        "language",
        "status",
        "created_by",
        "created_at",
        "updated_by",
        "updated_at",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = [
        "title",
    ]  # search by field name
    filterset_class = EmailTemplateFilter

    def perform_create(self, serializer):
        # print(self.request)
        serializer.save(created_by=self.request.user, created_at=timezone.now())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())


class NotiPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class NotificationAPIView(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = NotiPagination


# total unread notification by current user
class TotalUserNotiAPIView(APIView):
    def get(self, request):
        try:
            user_id = request.user.id
            unread_count = User.objects.get(id=user_id)
            return Response({"unread_count": unread_count.noti_count})
        except User.DoesNotExist:
            return 0


# unread_count = Notification.objects.filter(to_user=user, is_read=False).count()
# return Response({'unread_count': unread_count})


# listing unread notification by current user
class ListUnreadUserNotiAPIView(APIView):
    pagination_class = NotiPagination

    def get(self, request):
        user_id = request.user.id
        unread_noti = Notification.objects.filter(
            to_user=user_id, is_read=False
        ).order_by("-created_at")
        paginator = self.pagination_class()
        paginated_unread_noti = paginator.paginate_queryset(unread_noti, request)
        serializer = NotificationSerializer(paginated_unread_noti, many=True)
        return paginator.get_paginated_response(serializer.data)


# listing notification by current user
class ListAllUserNotiAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    pagination_class = NotiPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    ordering_fields = (
        "is_read",
        "created_at",
    )
    search_fields = (
        "from_user__first_name",
        "is_read",
    )
    filterset_class = NotificationFilter

    # fields = (
    # 	"from_user__first_name",
    # 	"is_read",
    # )
    # ordering_fields = fields  # ordering by field name
    # search_fields = fields  # search by field name
    # filterset_class = NotificationFilter

    def get_queryset(self):
        user_id = self.request.user.id

        order_param = self.request.query_params.get("ordering", None)

        queryset = Notification.objects.filter(to_user=user_id).order_by(
            F("is_read").asc(), "-created_at"
        )

        if order_param == "0":
            queryset = queryset.order_by("is_read")
        elif order_param == "1":
            queryset = queryset.order_by("-is_read")

        elif order_param is not None:
            raise ParseError(
                "Invalid ordering parameter. Use '0' for ascending or '1' for descending order."
            )
        else:
            queryset = queryset.order_by(F("is_read").asc(), "-created_at")

        return queryset


# update field is_read to True when click view notification listing
class ViewNotiByUserAPIView(APIView):
    @transaction.atomic
    def get(self, request, pk):
        try:
            user_id = request.user.id
            queryset = Notification.objects.get(id=pk, to_user=user_id)
            data = {"is_read": True}
            serializer = NotificationSerializer(
                instance=queryset, data=data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                GlobalHelper.decrease_user_unread_noti(user_id)
            return Response({"message": "success"})

        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                }
            )


class MakeReadAllByUserNotiAPIView(APIView):
    @transaction.atomic
    def get(self, request):
        try:
            user = request.user.id
            queryset = Notification.objects.filter(to_user=user)
            data = {"is_read": True}
            for notification in queryset:
                serializer = NotificationSerializer(
                    instance=notification, data=data, partial=True
                )
                if serializer.is_valid():
                    serializer.save()

            queryset_user = get_object_or_404(User, id=user)
            data_user = {"noti_count": 0}
            serializer_user = UserSerializer(
                instance=queryset_user, data=data_user, partial=True
            )
            if serializer_user.is_valid():
                serializer_user.save()

            return Response(
                {"success": True, "status": status.HTTP_200_OK, "message": "success"}
            )
        except ValidationError as e:
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": str(e),
                }
            )


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class OptionSelectUserListingViewSet(viewsets.ModelViewSet):
    serializer_class = UserListingNotiSerializer
    queryset = User.objects.all().order_by("-created_at")

    pagination_class = UserPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    fields = (
        "id",
        "staff_id",
        "username",
        "first_name",
        "last_name",
        "first_name_kh",
        "last_name_kh",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # search by field name
    filterset_class = UserOptionSelectFilter  # filter by field name

    # Disable create, update, partial update, and delete operations
    def create(self, request):
        return Response(
            {"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
