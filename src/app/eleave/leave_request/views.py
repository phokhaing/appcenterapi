from ..leave_reason.models import LeaveReasonModel
from rest_framework.decorators import api_view
from ..leave_balance.models import LeaveBalance
from ...user_notification.serializer import NotificationStoreSerializer
from ...user_notification.models import Notification
from ...utils import NotificationSending
from ...utils.EmailSending import (
    send_email_inbound,
    send_email_outbound,
    getEmailTemplateByHook,
)
from ...utils.GlobalHelper import GlobalHelper
from django.conf import settings
from ...utils.DoUpload import removeUploadedByName, doUploadFiles
from ...utils.UserAccessPermission import permission_required
import datetime
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse
from .filter import LeaveRequestFilter
from .serializer import (
    LeaveRequestSerializer,
    LeaveReasonSerializer,
    LeaveRequestListingSerializer,
    LeaveRequestFilterExportSerializer,
    LeaveRequestViewSerializer,
)
from .models import LeaveRequest
from ..leave_summary.serializer import LeaveRequestCertifierSerializer
from ..leave_type.models import LeaveTypeModel
from ..leave_file.serializer import LeaveFileSerializer
from django.db import transaction
from datetime import date
from django.contrib.auth import get_user_model
from app.utils.IdEncryption import IdEncryption
from ...utils.UserAccessPermission import permission_api_view_required

User = get_user_model()


# block import **** Notification and Email Setting ******

# from openpyxl import Workbook
# from django.http import HttpResponse
# import io

# End block import **** Notification and Email Setting ******

module_name = "ELEAVE/LEAVE_REQUEST"


class LeaveRequestPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UploadFilesView:
    @transaction.atomic
    def upload_items(self, attachment, user, instance, user_logged):
        if instance:
            # pathStore = f'eleave/attachment/staff_id/{user}/{instance}'
            pathStore = f"eleave/attachment"
            getUploaded = doUploadFiles(attachment, pathStore)
            file_serializer_list = []

            for file in getUploaded:
                file["leave_id"] = instance
                file["created_by"] = user_logged
                file["status"] = 1
                file_serializer_list.append(file)
                serializer_file = LeaveFileSerializer(data=file)
                if serializer_file.is_valid():
                    serializer_file.save()

            return file_serializer_list
        else:
            return []


def check_leave_balance(user_id):
    query = LeaveBalance.objects.filter(employee=user_id).order_by("-year").first()
    if query is not None:
        entitle_balance = query.entitle_balance
        if entitle_balance > 0:
            return True
        else:
            return None
    else:
        return None


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer

    pagination_class = LeaveRequestPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = ("id", "staff_id", "staff_name")
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # search by field name
    filterset_class = LeaveRequestFilter

    @api_view(["GET"])
    def listing_leave_request(request):
        user_id = request.GET.get("user_id")
        department = request.GET.get("department")
        branch = request.GET.get("branch")
        leave_status = request.GET.get("leave_status")
        leave_start_date = request.GET.get("leave_start_date")
        leave_end_date = request.GET.get("leave_end_date")

        leave_type = request.GET.get("leave_type")
        leave_year = request.GET.get("leave_year")

        leave_certified = request.GET.get("leave_certified")
        leave_authorized = request.GET.get("leave_authorized")

        search_fields = ["staff_id", "staff_name", "reason"]
        filter_fields = ["staff_id", "staff_name", "reason"]

        queryset = LeaveRequest.objects.all().order_by("-created_at")

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if department is not None:
            queryset = queryset.filter(user_id__department_id=department)

        if branch is not None:
            queryset = queryset.filter(user_id__branch_id=branch)

        if leave_type is not None:
            queryset = queryset.filter(leave_type__id=leave_type)

        if leave_status is not None:
            queryset = queryset.filter(leave_status__id=leave_status)

        if leave_certified is not None:
            queryset = queryset.filter(certifier_by_id=leave_certified)

        if leave_authorized is not None:
            queryset = queryset.filter(authorizer_by_id=leave_authorized)

        if leave_year is not None:
            leave_year_datetime = datetime.datetime.strptime(leave_year, "%Y")
            queryset = queryset.filter(end_date__year=leave_year_datetime.year)

        if leave_start_date and leave_end_date:
            start_date = datetime.datetime.strptime(
                leave_start_date, "%d-%m-%Y"
            ).strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(leave_end_date, "%d-%m-%Y").strftime(
                "%Y-%m-%d"
            )
            queryset = queryset.filter(end_date__range=(start_date, end_date))

        other_filter = bool(
            user_id
            or leave_type
            or leave_status
            or leave_start_date
            or leave_end_date
            or leave_certified
            or leave_authorized
            or leave_year
        )

        if not other_filter:
            today = date.today()
            queryset = queryset.filter(created_at__date=today)

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=LeaveRequestListingSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="Leave request list by user requested retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    @api_view(["GET"])
    def filter_export_leave_request(request):
        user_id = request.GET.get("user_id")
        department = request.GET.get("department")
        branch = request.GET.get("branch")
        leave_status = request.GET.get("leave_status")
        leave_start_date = request.GET.get("leave_start_date")
        leave_end_date = request.GET.get("leave_end_date")

        leave_type = request.GET.get("leave_type")
        leave_year = request.GET.get("leave_year")

        leave_certified = request.GET.get("leave_certified")
        leave_authorized = request.GET.get("leave_authorized")

        search_fields = ["staff_id", "staff_name", "reason"]
        filter_fields = ["staff_id", "staff_name", "reason"]

        # Check if only pagination parameters are provided without filtering parameters
        if all(
            value is None
            for value in [
                user_id,
                department,
                branch,
                leave_status,
                leave_start_date,
                leave_end_date,
                leave_type,
                leave_year,
                leave_certified,
                leave_authorized,
            ]
        ):
            # If only pagination parameters are provided, return an empty response
            return ApiResponse.success(
                message="No filtering parameters provided.", results=[], count=0
            )

        queryset = LeaveRequest.objects.all().order_by("-created_at")

        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)

        if department is not None:
            queryset = queryset.filter(user_id__department_id=department)

        if branch is not None:
            queryset = queryset.filter(user_id__branch_id=branch)

        if leave_type is not None:
            queryset = queryset.filter(leave_type__id=leave_type)

        if leave_status is not None:
            queryset = queryset.filter(leave_status__id=leave_status)

        if leave_year is not None:
            leave_year_datetime = datetime.datetime.strptime(leave_year, "%Y")
            queryset = queryset.filter(end_date__year=leave_year_datetime.year)

        if leave_certified is not None:
            queryset = queryset.filter(certifier_by_id=leave_certified)

        if leave_authorized is not None:
            queryset = queryset.filter(authorizer_by_id=leave_authorized)

        if leave_start_date and leave_end_date:
            start_date = datetime.datetime.strptime(
                leave_start_date, "%d-%m-%Y"
            ).strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(leave_end_date, "%d-%m-%Y").strftime(
                "%Y-%m-%d"
            )
            queryset = queryset.filter(end_date__range=(start_date, end_date))

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=LeaveRequestFilterExportSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 100),
        )

        return ApiResponse.success(
            message="Leave request list by user requested retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    @permission_required(module_name, "LIST")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @transaction.atomic
    @permission_required(module_name, "CREATE")
    def create(self, request, *args, **kwargs):
        global status_name, noti_message
        user_logged = request.user

        employee = GlobalHelper.find_user_info_by_user_id(
            int(request.data.get("user_id"))
        )  # print('employee': ['1'])

        if not employee:
            return Response(
                {"error": "Invalid employee information"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        #
        # leave_balance = check_leave_balance(employee['user_id'])
        #
        # if not leave_balance:
        # 	return Response({"error": "Your leave balance is insufficient. Please get in touch with your line manager or HR department. Thanks"},
        # 	                status=status.HTTP_400_BAD_REQUEST)

        module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_REQUEST")

        if not module_data:
            return Response(
                {"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST
            )

        email_template = getEmailTemplateByHook(
            "ELEAVE_LEAVE_REQUEST"
        )  # get hook email
        if not email_template:
            return Response(
                {"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST
            )

        start_date = datetime.datetime.strptime(
            request.data["start_date"], "%d-%m-%Y"
        ).strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(
            request.data["end_date"], "%d-%m-%Y"
        ).strftime("%Y-%m-%d")

        incharge_request = "N"
        incharge_certifier = (
            "N" if request.data.get("incharge_certifier") == "false" else "Y"
        )
        incharge_authorizer = (
            "N" if request.data.get("incharge_authorizer") == "false" else "Y"
        )

        hour = request.data["hours"]
        minute = request.data["minute"]

        convert_hour_to_minute = 60 * float(hour)
        total_time = convert_hour_to_minute + float(minute)

        certifier = GlobalHelper.find_user_info_by_user_id(request.data["certifier"])
        authorizer = GlobalHelper.find_user_info_by_user_id(request.data["authorizer"])
        leave_type = GlobalHelper.find_leave_type_by_hook_name(
            request.data["leave_type"]
        )

        # ********** for view test data get value *************#
        context = {
            # information of user request take leave
            "user_id": employee["user_id"],
            "staff_id": employee["staff_id"],
            "staff_name": employee["full_name"],
            "staff_position": employee["position"],
            "staff_department": employee["department"],
            "leave_type": leave_type.id,
            "start_date": start_date,
            "end_date": end_date,
            "from_time": request.data["from_time"],
            "to_time": request.data["to_time"],
            "hours": request.data["hours"],
            "minute": minute,
            "total_time": total_time,
            "certifier": certifier["user_id"],
            "authorizer": authorizer["user_id"],
            "incharge_request": incharge_request,
            "incharge_certifier": incharge_certifier,
            "incharge_authorizer": incharge_authorizer,
            "reason": request.data["reason"],
            "leave_status": 2,  # requested
            "requested_by": user_logged.id,
            "requested_at": datetime.datetime.now(),
            "created_by": user_logged.id,
        }

        serializer = LeaveRequestSerializer(data=context)
        if serializer.is_valid():
            instance = serializer.save()
            # assign certified if both certifier and approve
            if certifier["user_id"] == authorizer["user_id"]:
                data = {
                    "certifier_by": certifier["user_id"],
                    "certifier_at": datetime.datetime.now(),
                    "leave_status": 3,  # status id certifier|Accepted
                }
                serializer_certified = LeaveRequestCertifierSerializer(
                    instance, data=data, partial=True
                )
                if serializer_certified.is_valid():
                    serializer_certified.save()
                    noti_message = "has been send request leave to you for approve."
                    status_name = "approve"
            else:
                noti_message = "has been send request leave to you for certify."
                status_name = "certify"

            # ****** Do upload files ******#
            if "attachment_files_upload" in request.data:
                files = request.data["attachment_files_upload"]
                if files:
                    attachment = request.FILES.getlist("attachment_files_upload") or []
                    staff_id = employee["staff_id"]
                    upload_files = UploadFilesView()
                    upload_files.upload_items(
                        attachment, staff_id, instance.id, user_logged.id
                    )
            # ****** End Do upload files ******#

            # ****** Send Notification ******#
            pk_encrypt = IdEncryption.encrypt_id(instance.id)
            url = f"/admin/eleave/leave_summary/view/{pk_encrypt}"
            # noti_message = 'has been send request leave to you for certifier.'
            data_notification = {
                "from_user": employee["user_id"],  # user requested
                "to_user": certifier["user_id"],  # to user by id
                # "url": 'admin/eleave/leave_summary',
                "url": url,
                "message": noti_message,  # message send to notification
                # recode id (input your primary key row data)
                "record_id": instance.id,
                # module id (input your moduleID)
                "module_id": module_data.id,
                "is_read": False,  # unread
            }

            serializer_notification = NotificationStoreSerializer(
                data=data_notification
            )
            if serializer_notification.is_valid():
                serializer_notification.save()

                # increase unread notification by user
                unread_count = GlobalHelper.increase_user_unread_noti(
                    certifier["user_id"]
                )

                # message = unread_count  # return count unread to client
                message = {
                    "total_unread": unread_count,
                    "message": employee["full_name"] + " " + noti_message,
                }

                NotificationSending.send_notification_to_user(
                    certifier["user_id"], message
                )

                display_hour = None
                display_minute = None

                hour_int = int(hour)
                minute_int = int(minute)

                if hour_int > 0:
                    display_hour = f"{hour_int} hour"

                if minute_int > 0:
                    display_minute = f" {minute_int} minute"

                if display_hour is None:
                    display_hour = ""

                if display_minute is None:
                    display_minute = ""

                total_time = display_hour + display_minute

                # *** Send Mail *** #
                # template_title = email_template.title
                # template_message = email_template.message
                # message_body = {
                #     "[FROM_USER]": employee["full_name"],
                #     "[TO_USER]": certifier["full_name"],
                #     "[REQUESTOR]": employee["full_name"],
                #     "[SITE_URL]": settings.DOMAIN_WEB + url,
                #     "[SITE_NAME]": settings.SITE_NAME,
                #     "[STATUS]": status_name,
                #     "[LEAVE_TYPE]": leave_type.name,
                #     "[FROM_DATE]": request.data["start_date"],
                #     "[TO_DATE]": request.data["end_date"],
                #     "[FROM_TIME]": request.data["from_time"],
                #     "[TO_TIME]": request.data["to_time"],
                #     "[TOTAL_TIME]": total_time,
                #     "[REASON]": request.data["reason"],
                # }
                # user_template_message = template_message
                # # Replace the keywords in the user-specific message
                # for keyword, replacement in message_body.items():
                #     user_template_message = user_template_message.replace(
                #         keyword, replacement
                #     )
                # # send email inbound configuration
                # send_email_inbound(
                #     template_title, user_template_message, certifier["email"]
                # )

                
            return Response(
                {
                    "message": "Leave request has been created",
                    "results": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(["GET"])
    @permission_api_view_required(module_name, "VIEW")
    def view_leave_request(request, pk):
        # Get back id from IdEncryption
        id = IdEncryption.decrypt_id(pk)

        if not LeaveRequest.objects.filter(id=id).exists():
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Leave request not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            instance = LeaveRequest.objects.get(id=id)
            serializer = LeaveRequestViewSerializer(instance)
            return Response(serializer.data)
        except LeaveRequest.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "status": status.HTTP_404_NOT_FOUND,
                    "message": "Leave request not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    # @permission_required(module_name, "VIEW")
    # def retrieve(self, request, *args, **kwargs):
    #     id = kwargs.get("pk")
    #     id = IdEncryption.decrypt_id(id)

    #     if not LeaveRequest.objects.filter(id=id).exists():
    #         return Response(
    #             {
    #                 "success": False,
    #                 "status": status.HTTP_404_NOT_FOUND,
    #                 "message": "Assessment not found.",
    #             },
    #             status=status.HTTP_404_NOT_FOUND,
    #         )

    #     instance = self.get_object()
    #     serializer = LeaveRequestViewSerializer(instance)
    #     return Response(serializer.data)

    @permission_required(module_name, "UPDATE")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(module_name, "UPDATE")
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(module_name, "DELETE")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


def get_manager_from_user(user_id):
    instance = User.objects.filter(id=user_id).first()
    if instance:
        data = {
            "user_id": instance.id,
            "staff_id": instance.staff_id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "fullname": f"{instance.first_name} {instance.last_name}",
            "manager": instance.manager.id if instance.manager else None,
        }
        return data
    else:
        return []


class FetchUserCertifyAuthorize(APIView):
    def get(self, request):
        user_logged = request.user
        certify = get_manager_from_user(user_logged.manager)
        authorize = get_manager_from_user(certify["manager"])

        context = {
            "certify": certify,
            "authorize": authorize,
        }
        # print("context:", context)
        return Response(
            {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "success",
                "data": context,
            }
        )


@api_view(["GET"])
def list_data_default_form(request):
    user = request.user
    certifier = get_manager_from_user(user.id)
    authorizer = get_manager_from_user(certifier["manager"])
    date_obj = datetime.date.today()
    today = date_obj.strftime("%d-%m-%Y")

    certifier_manager = certifier.get("manager") if certifier else None
    authorizer_manager = authorizer.get("manager") if authorizer else None

    context = {
        "employee": user.id,
        "leave_type": "ANNUAL_LEAVE",
        "start_date": today,
        "end_date": today,
        "from_time": "08:00",
        "to_time": "17:00",
        "hours": 8,
        "minute": 0,
        "certifier": None,
        # 'certifier': certifier_manager,
        "authorizer": None,
        # 'authorizer': authorizer_manager,
        "reason": "",
    }
    response = {"message": "success", "data": context}
    return Response(data=response, status=status.HTTP_200_OK)


@api_view(["GET"])
def list_leave_reason(request):
    try:
        queryset = LeaveReasonModel.objects.all()
        serializer = LeaveReasonSerializer(queryset, many=True)
        response = {"message": "success", "data": serializer.data}
    except LeaveReasonModel.DoesNotExist:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response, status=status.HTTP_200_OK)
