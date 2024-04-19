from django.shortcuts import get_object_or_404

# from rest_framework import generics, mixins, status
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, parser_classes, APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import (
    LeaveRequestSummarySerializer,
    LeaveBalanceSummarySerializer,
    LeaveRequestCertifierSerializer,
    LeaveRequestApproveSerializer,
    LeaveRequestRejectSerializer,
    LeaveRequestStatusSerializer,
    LeaveRequestCancelSerializer,
    CustomPaginationSerializer,
)
from ..leave_balance.models import LeaveBalance
from ..leave_balance.serializer import LeaveBalanceSerializer
from ..leave_file.serializer import LeaveFileSerializer
from ..leave_file.models import LeaveFile
from ..leave_request.models import LeaveRequest, LeaveRequestStatus
from django.db.models import Q
from django.db import transaction
from datetime import datetime, timedelta

# Global Helpers
from ...utils.GlobalHelper import GlobalHelper
from ...utils.EmailSending import (
    send_email_inbound,
    send_email_outbound,
    getEmailTemplateByHook,
)
from ...utils import NotificationSending
from django.conf import settings
from ...user_notification.serializer import NotificationStoreSerializer
from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse
from ...utils.global_openapi_schema import (
    global_request_openapi_schema,
    global_response_openapi_shema,
)
from django.core.paginator import Paginator
from rest_framework.exceptions import ValidationError
from .query import query_fetch_leave_request
from app.utils.IdEncryption import IdEncryption
from django.contrib.auth import get_user_model
from ..leave_type.models import LeaveTypeModel

User = get_user_model()


class LeaveSummaryController:

    @swagger_auto_schema(
        method="GET",
        operation_description="Retrieve a list of summary with pagination, search and filtering",
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
                name="current_user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by current_user",
                required=False,
            ),
            openapi.Parameter(
                name="default",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by default (1=get data from query)(2=get history data)",
                required=False,
            ),
            openapi.Parameter(
                name="leave_type",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_type",
                required=False,
            ),
            openapi.Parameter(
                name="leave_status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_status",
                required=False,
            ),
            openapi.Parameter(
                name="leave_start_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_start_date",
                required=False,
            ),
            openapi.Parameter(
                name="leave_end_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_end_date",
                required=False,
            ),
        ],
    )
    @api_view(["GET"])
    def listing_leave_request_by_user(request):
        # user = request.user
        user_request = request.GET.get("current_user")
        default = request.GET.get("default")
        leave_type = request.GET.get("leave_type")
        leave_status = request.GET.get("leave_status")
        leave_start_date = request.GET.get("leave_start_date")
        leave_end_date = request.GET.get("leave_end_date")
        # Listing data from query
        if default == "1":
            all_query = query_fetch_leave_request(user_request)

            class CustomPageNumberPagination(PageNumberPagination):
                page_size = 10
                page_size_query_param = "page_size"
                max_page_size = 100

            paginator = CustomPageNumberPagination()
            result_page = paginator.paginate_queryset(all_query, request)

            data_pending = []
            for data in result_page:
                data["requested_by"] = GlobalHelper.show_user_fullname_en(
                    data["requested_by"]
                )
                data["certifier"] = GlobalHelper.show_user_fullname_en(
                    data["certifier"]
                )
                data["certifier_by"] = GlobalHelper.show_user_fullname_en(
                    data["certifier_by"]
                )
                data["authorizer"] = GlobalHelper.show_user_fullname_en(
                    data["authorizer"]
                )
                data["authorizer_by"] = GlobalHelper.show_user_fullname_en(
                    data["authorizer_by"]
                )
                data["rejected_by"] = GlobalHelper.show_user_fullname_en(
                    data["rejected_by"]
                )
                data["created_by"] = GlobalHelper.show_user_fullname_en(
                    data["created_by"]
                )
                data["staff_gender"] = LeaveSummaryController.get_staff_gender(
                    data["user_id"]
                )
                data["leave_type"] = LeaveSummaryController.get_leave_type(
                    data["leave_type"]
                )
                data["leave_status"] = LeaveSummaryController.get_leave_status(
                    data["leave_status"]
                )
                data["current_annual_leave_by_hour"] = (
                    LeaveSummaryController.get_current_annual_leave_by_hour(
                        data["user_id"]
                    )
                )
                data["encrypt_key"] = LeaveSummaryController.get_encrypt_key(data["id"])
                data["staff_avatar"] = GlobalHelper.find_user_avatar_by_user_id(
                    data["user_id"]
                )
                data["leave_files"] = LeaveSummaryController.get_leave_files(data["id"])

                data_pending.append(data)

            serializer = CustomPaginationSerializer(
                {
                    "count": paginator.page.paginator.count,
                    "page": paginator.page.number,
                    "pages": paginator.page.paginator.num_pages,
                    "page_size": paginator.page.paginator.per_page,
                    "next_page": (
                        paginator.page.next_page_number()
                        if paginator.page.has_next()
                        else None
                    ),
                    "next_page_url": paginator.get_next_link(),
                    "previous_page": (
                        paginator.page.previous_page_number()
                        if paginator.page.has_previous()
                        else None
                    ),
                    "previous_page_url": paginator.get_previous_link(),
                }
            )

            if len(all_query) > 0:
                response_data = {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "List data success",
                    "count": paginator.page.paginator.count,
                    "next": paginator.get_next_link(),
                    "previous": paginator.get_previous_link(),
                    "results": data_pending,
                    "paginators": serializer.data,
                }
                return Response(response_data)
            else:
                return Response(
                    {
                        "success": True,
                        "status": status.HTTP_200_OK,
                        "message": "No data",
                        "count": len(data_pending),
                        "next": None,
                        "previous": None,
                        "results": [],
                    }
                )

        elif default == "2":
            queryset = LeaveRequest.objects.filter(Q(user_id=user_request)).order_by(
                "-created_at"
            )
            if leave_type is not None:
                queryset = queryset.filter(leave_type__id=leave_type)

            if leave_status is not None:
                queryset = queryset.filter(leave_status__id=leave_status)

            if leave_start_date and leave_end_date:
                start_date = datetime.strptime(leave_start_date, "%d-%m-%Y").strftime(
                    "%Y-%m-%d"
                )
                end_date = datetime.strptime(leave_end_date, "%d-%m-%Y").strftime(
                    "%Y-%m-%d"
                )
                queryset = queryset.filter(end_date__range=(start_date, end_date))

            search_fields = ["staff_id", "staff_name", "reason"]
            filter_fields = ["staff_id", "staff_name", "reason"]

            paginator = PaginatorResponse(
                queryset=queryset,
                request=request,
                serializer_class=LeaveRequestSummarySerializer,
                search_fields=search_fields,
                filter_fields=filter_fields,
                page_size=request.GET.get("page_size", 10),
            )
            return ApiResponse.success(
                message="Data retrieved successfully",
                results=paginator.paginator_results(),
                paginators=paginator.api_response_paginators(),
                count=paginator.paginator_count(),
                next=paginator.paginator_next(),
                previous=paginator.paginator_previous(),
            )

        else:
            search_fields = ["staff_id", "staff_name", "reason"]
            filter_fields = ["staff_id", "staff_name", "reason"]

            queryset = LeaveRequest.objects.none()  # Empty queryset
            paginator = PaginatorResponse(
                queryset=queryset,
                request=request,
                serializer_class=LeaveRequestSummarySerializer,
                search_fields=search_fields,
                filter_fields=filter_fields,
                page_size=request.GET.get("page_size", 10),
            )
            return ApiResponse.success(
                message="Data retrieved successfully",
                results=paginator.paginator_results(),
                paginators=paginator.api_response_paginators(),
                count=paginator.paginator_count(),
                next=paginator.paginator_next(),
                previous=paginator.paginator_previous(),
            )

    @swagger_auto_schema(
        method="GET",
        operation_description="Fetch listing_leave_approval_by_user pagination, search and filtering",
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
                name="current_user",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by current_user",
                required=False,
            ),
            openapi.Parameter(
                name="default",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by default (1=get padding cerity and approve)(2=get history data ceritied and approved)",
                required=False,
            ),
            openapi.Parameter(
                name="leave_type",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_type",
                required=False,
            ),
            openapi.Parameter(
                name="leave_status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_status",
                required=False,
            ),
            openapi.Parameter(
                name="leave_start_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_start_date",
                required=False,
            ),
            openapi.Parameter(
                name="leave_end_date",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by leave_end_date",
                required=False,
            ),
            openapi.Parameter(
                name="staff_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by staff_id",
                required=False,
            ),
        ],
    )
    @api_view(["GET"])
    def listing_leave_approval_by_user(request):
        # user = request.user
        user_request = request.GET.get("current_user")
        default = request.GET.get("default")
        leave_type = request.GET.get("leave_type")
        leave_status = request.GET.get("leave_status")
        user_id = request.GET.get("user_id")
        leave_start_date = request.GET.get("leave_start_date")
        leave_end_date = request.GET.get("leave_end_date")

        # Listing data padding certify and approve
        if default == "1":
            current_year = datetime.now().year
            previous_year = current_year - 1

            # print("current_year:", current_year)
            # print("previous_year:", previous_year)

            queryset1 = LeaveRequest.objects.filter(
                Q(certifier=user_request)
                & Q(certifier_by__isnull=True)
                & Q(rejected_by__isnull=True)
                & Q(canceled_by__isnull=True)
                & Q(authorizer_by__isnull=True)
                & Q(start_date__year__gte=previous_year)  # Filter from previous year
            )

            queryset2 = LeaveRequest.objects.filter(
                Q(certifier_by__isnull=False)
                & Q(authorizer=user_request)
                & Q(authorizer_by__isnull=True)
                & Q(rejected_by__isnull=True)
                & Q(canceled_by__isnull=True)
                & Q(start_date__year__gte=previous_year)  # Filter from previous year
            )
            merged_queryset = queryset1 | queryset2
            queryset = merged_queryset.order_by("-created_at")

        # listing filter data history of current user approve
        elif default == "2":
            queryset = LeaveRequest.objects.filter(
                Q(certifier=user_request)
                | Q(certifier_by=user_request)
                | Q(authorizer=user_request)
                | Q(authorizer_by=user_request)
            ).order_by("-created_at")

            if leave_type is not None:
                queryset = queryset.filter(leave_type__id=leave_type)

            if leave_status is not None:
                queryset = queryset.filter(leave_status__id=leave_status)

            if user_id is not None:
                queryset = queryset.filter(user_id=user_id)

            if leave_start_date and leave_end_date:
                start_date = datetime.strptime(leave_start_date, "%d-%m-%Y").strftime(
                    "%Y-%m-%d"
                )
                end_date = datetime.strptime(leave_end_date, "%d-%m-%Y").strftime(
                    "%Y-%m-%d"
                )
                queryset = queryset.filter(end_date__range=(start_date, end_date))

        else:
            queryset = LeaveRequest.objects.none()  # Empty queryset

        search_fields = ["staff_id", "staff_name", "reason"]
        filter_fields = ["staff_id", "staff_name", "reason"]

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=LeaveRequestSummarySerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="Pending approval retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    @api_view(["GET"])
    def listing_leave_balance_by_user(request):
        user = request.user
        try:
            queryset = (
                LeaveBalance.objects.filter(employee=user.id).order_by("-year").first()
            )
            if queryset:
                serializer = LeaveBalanceSummarySerializer(queryset)
                return ApiResponse.success(
                    message="Leave summary balance by user retrieved successfully.",
                    results=serializer.data,
                )
            else:
                return ApiResponse.not_found()
        except LeaveBalance.DoesNotExist:
            return ApiResponse.not_found()

    @api_view(["PUT"])
    @transaction.atomic
    def certifier_authorize_by_user(request, record_id):
        user = request.user
        try:
            queryset = get_object_or_404(LeaveRequest, pk=record_id)
        except LeaveRequest.DoesNotExist:
            return ApiResponse.not_found()

        module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_SUMMARY")
        if not module_data:
            return Response(
                {"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST
            )

        email_template = getEmailTemplateByHook(
            "ELEAVE_LEAVE_CERTIFY"
        )  # get hook email
        if not email_template:
            return Response(
                {"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "certifier_by": user.id,
            "certifier_at": datetime.now(),
            "leave_status": 3,  # status id certifier|Accepted
        }
        serializer = LeaveRequestCertifierSerializer(
            instance=queryset, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            from_user = GlobalHelper.find_user_info_by_user_id(user.id)
            requestor = GlobalHelper.find_user_info_by_user_id(queryset.user_id.id)

            # send mail and notification to user requestor
            noti_message = f"have been certified your leave request."
            # url = f"/admin/eleave/leave_summary"
            pk_encrypt = IdEncryption.encrypt_id(queryset.id)
            url = f"/admin/eleave/leave_summary/view/{pk_encrypt}"
            email_hook = f"ELEAVE_LEAVE_REQUESTOR"
            status_name = f"Certified"

            LeaveSummaryController.send_notification(
                from_user["user_id"],
                requestor["user_id"],
                queryset.id,
                module_data.id,
                noti_message,
                url,
                queryset,
                status_name,
            )

            LeaveSummaryController.send_email(
                from_user["user_id"],
                requestor["user_id"],
                queryset.id,
                module_data.id,
                url,
                email_hook,
                queryset,
                status_name,
            )

            # send mail and notification to user approval
            requestor_full_name = requestor["full_name"]
            user_approve = GlobalHelper.find_user_info_by_user_id(
                queryset.authorizer.id
            )
            noti_message_approve = f"have been sent leave request of user {requestor_full_name} to you for approve."
            email_hook_approve = f"ELEAVE_LEAVE_CERTIFY"
            status_name_approve = f"Approve"

            LeaveSummaryController.send_notification(
                from_user["user_id"],
                user_approve["user_id"],
                queryset.id,
                module_data.id,
                noti_message_approve,
                url,
                queryset,
                status_name_approve,
            )

            LeaveSummaryController.send_email(
                from_user["user_id"],
                user_approve["user_id"],
                queryset.id,
                module_data.id,
                url,
                email_hook_approve,
                queryset,
                status_name_approve,
            )

            return ApiResponse.success(
                message="Certified successfully.",
                results=serializer.data,
            )

        return ApiResponse.error(errors=serializer.errors)

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

    # check employee of leave balance specific year
    # prevent if user not have year balance
    def check_leave_balance_by_year(user_id, request_date, year):
        if request_date == year:
            query = LeaveBalance.objects.filter(
                Q(employee=user_id) & Q(year=year)
            ).first()
            if query is not None:
                return True
            else:
                return False
        else:
            return False

    @transaction.atomic
    def calculate_leave_balance(
        user_id, record_id, total_time, leave_type, request_date_year
    ):
        # check balance requested input end date with balance of year user
        check_balance_by_year = LeaveBalance.objects.filter(
            Q(employee=user_id) & Q(year=request_date_year)
        ).first()

        if check_balance_by_year is not None:
            query = check_balance_by_year
        else:
            # if not found, it will get old leave balance back year to calculate
            query = (
                LeaveBalance.objects.filter(employee=user_id).order_by("-year").first()
            )

        try:
            if query is not None:
                if str(leave_type) == "ANNUAL_LEAVE":
                    begin_annual_leave = query.begin_annual_leave
                    taken_annual_leave = query.taken_annual_leave
                    current_annual_leave = query.current_annual_leave

                    total_taken_annual_leave = float(taken_annual_leave) + float(
                        total_time
                    )
                    # total_current_annual_leave = float(begin_annual_leave) - float(
                    #     total_taken_annual_leave
                    # )

                    total_current_annual_leave = float(current_annual_leave) - float(
                        total_time
                    )

                    data = {
                        "taken_annual_leave": round(total_taken_annual_leave),
                        "current_annual_leave": round(total_current_annual_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance ANNUAL_LEAVE"}
                        )

                elif str(leave_type) == "SICK_LEAVE":
                    begin_sick_leave = query.begin_sick_leave
                    taken_sick_leave = query.taken_sick_leave
                    current_sick_leave = query.current_sick_leave

                    total_taken_sick_leave = float(taken_sick_leave) + float(total_time)
                    # total_current_sick_leave = float(begin_sick_leave) - float(
                    #     total_taken_sick_leave
                    # )

                    total_current_sick_leave = float(current_sick_leave) - float(
                        total_time
                    )

                    data = {
                        "taken_sick_leave": round(total_taken_sick_leave),
                        "current_sick_leave": round(total_current_sick_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance SICK_LEAVE"}
                        )

                elif str(leave_type) == "SPECIAL_LEAVE":
                    begin_special_leave = query.begin_special_leave
                    taken_special_leave = query.taken_special_leave
                    current_special_leave = query.current_special_leave

                    total_taken_special_leave = float(taken_special_leave) + float(
                        total_time
                    )
                    # total_current_special_leave = float(begin_special_leave) - float(
                    #     total_taken_special_leave
                    # )

                    total_current_special_leave = float(current_special_leave) - float(
                        total_time
                    )

                    data = {
                        "taken_special_leave": round(total_taken_special_leave),
                        "current_special_leave": round(total_current_special_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance SPECIAL_LEAVE"}
                        )

                elif str(leave_type) == "MATERNITY_LEAVE":
                    begin_maternity_leave = query.begin_maternity_leave
                    taken_maternity_leave = query.taken_maternity_leave
                    current_maternity_leave = query.current_maternity_leave

                    total_taken_maternity_leave = float(taken_maternity_leave) + float(
                        total_time
                    )
                    # total_current_maternity_leave = float(
                    #     begin_maternity_leave
                    # ) - float(total_taken_maternity_leave)

                    total_current_maternity_leave = float(
                        current_maternity_leave
                    ) - float(total_time)

                    data = {
                        "taken_maternity_leave": round(total_taken_maternity_leave),
                        "current_maternity_leave": round(total_current_maternity_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance MATERNITY_LEAVE"}
                        )

                elif str(leave_type) == "UNPAID_LEAVE":
                    begin_unpaid_Leave = query.begin_unpaid_Leave
                    taken_unpaid_leave = query.taken_unpaid_leave
                    current_unpaid_leave = query.current_unpaid_leave

                    total_taken_unpaid_leave = float(taken_unpaid_leave) + float(
                        total_time
                    )
                    # total_current_unpaid_leave = float(begin_unpaid_Leave) - float(
                    #     total_taken_unpaid_leave
                    # )

                    total_current_unpaid_leave = float(current_unpaid_leave) - float(
                        total_time
                    )

                    data = {
                        "taken_unpaid_leave": round(total_taken_unpaid_leave),
                        "current_unpaid_leave": round(total_current_unpaid_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance UNPAID_LEAVE"}
                        )

                else:
                    raise ValidationError({"Leave type Invalided"})
            else:
                raise ValidationError({"query Invalided"})

        except ValidationError as e:
            ValidationError({e})

    @transaction.atomic
    def calculate_leave_balance_cancel(
        user_id, record_id, total_time, leave_type, request_date_year
    ):
        # check balance requested input end date with balance of year user
        check_balance_by_year = LeaveBalance.objects.filter(
            Q(employee=user_id) & Q(year=request_date_year)
        ).first()

        if check_balance_by_year is not None:
            query = check_balance_by_year
        else:
            # if not found, it will get old leave balance back year to calculate
            query = (
                LeaveBalance.objects.filter(employee=user_id).order_by("-year").first()
            )
        try:
            if query is not None:
                if str(leave_type) == "ANNUAL_LEAVE":
                    begin_annual_leave = query.begin_annual_leave
                    taken_annual_leave = query.taken_annual_leave
                    current_annual_leave = query.current_annual_leave
                    total_taken_annual_leave = float(taken_annual_leave) - float(
                        total_time
                    )
                    total_current_annual_leave = float(current_annual_leave) + float(
                        total_time
                    )

                    data = {
                        "taken_annual_leave": round(total_taken_annual_leave),
                        "current_annual_leave": round(total_current_annual_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance ANNUAL_LEAVE"}
                        )

                elif str(leave_type) == "SICK_LEAVE":
                    begin_sick_leave = query.begin_sick_leave
                    taken_sick_leave = query.taken_sick_leave
                    current_sick_leave = query.current_sick_leave

                    total_taken_sick_leave = float(taken_sick_leave) - float(total_time)
                    total_current_sick_leave = float(current_sick_leave) + float(
                        total_time
                    )

                    data = {
                        "taken_sick_leave": round(total_taken_sick_leave),
                        "current_sick_leave": round(total_current_sick_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance SICK_LEAVE"}
                        )
                elif str(leave_type) == "SPECIAL_LEAVE":
                    begin_special_leave = query.begin_special_leave
                    taken_special_leave = query.taken_special_leave
                    current_special_leave = query.current_special_leave

                    total_taken_special_leave = float(taken_special_leave) - float(
                        total_time
                    )
                    total_current_special_leave = float(current_special_leave) + float(
                        total_time
                    )

                    data = {
                        "taken_special_leave": round(total_taken_special_leave),
                        "current_special_leave": round(total_current_special_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance SPECIAL_LEAVE"}
                        )
                elif str(leave_type) == "MATERNITY_LEAVE":
                    begin_maternity_leave = query.begin_maternity_leave
                    taken_maternity_leave = query.taken_maternity_leave
                    current_maternity_leave = query.current_maternity_leave

                    total_taken_maternity_leave = float(taken_maternity_leave) - float(
                        total_time
                    )
                    total_current_maternity_leave = float(
                        current_maternity_leave
                    ) + float(total_time)

                    data = {
                        "taken_maternity_leave": round(total_taken_maternity_leave),
                        "current_maternity_leave": round(total_current_maternity_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance MATERNITY_LEAVE"}
                        )
                elif str(leave_type) == "UNPAID_LEAVE":
                    begin_unpaid_Leave = query.begin_unpaid_Leave
                    taken_unpaid_leave = query.taken_unpaid_leave
                    current_unpaid_leave = query.current_unpaid_leave

                    total_taken_unpaid_leave = float(taken_unpaid_leave) - float(
                        total_time
                    )
                    total_current_unpaid_leave = float(current_unpaid_leave) + float(
                        total_time
                    )

                    data = {
                        "taken_unpaid_leave": round(total_taken_unpaid_leave),
                        "current_unpaid_leave": round(total_current_unpaid_leave),
                    }

                    serializer = LeaveBalanceSerializer(
                        instance=query, data=data, partial=True
                    )
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        raise ValidationError(
                            {"serializer error update leave balance UNPAID_LEAVE"}
                        )
                else:
                    raise ValidationError({"Leave type Invalided"})
        except ValidationError as e:
            ValidationError({e})

    @api_view(["PUT"])
    @transaction.atomic
    def approve_authorize_by_user(request, record_id):
        user = request.user
        try:
            queryset = get_object_or_404(LeaveRequest, pk=record_id)
        except LeaveRequest.DoesNotExist:
            return ApiResponse.not_found()

        employee_id = queryset.user_id.id
        request_date_year = queryset.end_date.year
        # Prevent approve if staff not have balance by year
        # current_year = datetime.now().year
        # leave_balance_year = LeaveSummaryController.check_leave_balance_by_year(employee_id, request_date_year, current_year)
        # if not leave_balance_year:
        # 	return Response(
        # 		{
        # 			"error": f"Sorry, this user does not have leave balance of {request_date_year}. Please contact the HR department for details."
        # 		},
        # 		status=status.HTTP_400_BAD_REQUEST,
        # 	)
        # leave_balance = LeaveSummaryController.check_leave_balance(employee_id)
        #
        # if not leave_balance:
        #     return Response(
        #         {"error": "Sorry user not have enough leave balance, cannot approve!"},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        receiver = GlobalHelper.find_user_info_by_user_id(employee_id)
        sender = GlobalHelper.find_user_info_by_user_id(user.id)

        if not receiver and sender:
            return Response(
                {"error": "Invalid receiver and sender information"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_SUMMARY")
        if not module_data:
            return Response(
                {"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST
            )

        email_template = getEmailTemplateByHook(
            "ELEAVE_LEAVE_APPROVE"
        )  # get hook email
        if not email_template:
            return Response(
                {"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "authorizer_by": user.id,
            "authorizer_at": datetime.now(),
            "leave_status": 7,  # status id authorized|Authorized
        }

        total_time = queryset.total_time
        employee = queryset.user_id
        leave_type = queryset.leave_type.HOOK_KEY

        # LeaveSummaryController.calculate_leave_balance(employee, record_id, total_time, leave_type, request_date_year)
        # return False

        serializer = LeaveRequestApproveSerializer(
            instance=queryset, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            LeaveSummaryController.calculate_leave_balance(
                employee, record_id, total_time, leave_type, request_date_year
            )

            noti_message = f"have been approved your leave request."
            # url = f"/admin/eleave/leave_summary"
            pk_encrypt = IdEncryption.encrypt_id(queryset.id)
            url = f"/admin/eleave/leave_summary/view/{pk_encrypt}"
            email_hook = f"ELEAVE_LEAVE_APPROVE"
            status_name = f"Approved"

            LeaveSummaryController.send_notification(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                noti_message,
                url,
                queryset,
                status_name,
            )

            LeaveSummaryController.send_email(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                url,
                email_hook,
                queryset,
                status_name,
            )

            return ApiResponse.success(
                message="Approved successfully.",
                results=serializer.data,
            )

        return ApiResponse.error(errors=serializer.errors)

    @api_view(["PUT"])
    @transaction.atomic
    def reject_authorize_by_user(request, record_id, *args, **kwargs):
        user = request.user
        try:
            queryset = get_object_or_404(LeaveRequest, pk=record_id)
        except LeaveRequest.DoesNotExist:
            return ApiResponse.not_found()

        receiver = GlobalHelper.find_user_info_by_user_id(queryset.user_id.id)
        sender = GlobalHelper.find_user_info_by_user_id(user.id)

        if not receiver and sender:
            return Response(
                {"error": "Invalid receiver and sender information"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_SUMMARY")
        if not module_data:
            return Response(
                {"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST
            )

        email_template = getEmailTemplateByHook("ELEAVE_LEAVE_REJECT")  # get hook email
        if not email_template:
            return Response(
                {"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "rejected_by": user.id,
            "rejected_at": datetime.now(),
            "rejected_reason": request.data.get("reason"),
            "leave_status": 4,  # status id rejected|Rejected
        }
        serializer = LeaveRequestRejectSerializer(
            instance=queryset, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

            noti_message = f"have been rejected your leave request."
            # url = f"/admin/eleave/leave_summary"
            pk_encrypt = IdEncryption.encrypt_id(queryset.id)
            url = f"/admin/eleave/leave_summary/view/{pk_encrypt}"
            email_hook = f"ELEAVE_LEAVE_REJECT"
            status_name = f"Rejected"

            LeaveSummaryController.send_notification(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                noti_message,
                url,
                queryset,
                status_name,
            )

            LeaveSummaryController.send_email(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                url,
                email_hook,
                queryset,
                status_name,
            )

            return ApiResponse.success(
                message="Rejected successfully.",
                results=serializer.data,
            )

        return ApiResponse.error(errors=serializer.errors)

    @api_view(["PUT"])
    @transaction.atomic
    def cancel_authorize_by_user(request, record_id, *args, **kwargs):
        user = request.user
        try:
            queryset = get_object_or_404(LeaveRequest, pk=record_id)
        except LeaveRequest.DoesNotExist:
            return ApiResponse.not_found()

        receiver = GlobalHelper.find_user_info_by_user_id(queryset.user_id.id)
        sender = GlobalHelper.find_user_info_by_user_id(user.id)

        if not receiver and sender:
            return Response(
                {"error": "Invalid receiver and sender information"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_SUMMARY")
        if not module_data:
            return Response(
                {"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST
            )

        email_template = getEmailTemplateByHook("ELEAVE_LEAVE_CANCEL")  # get hook email
        if not email_template:
            return Response(
                {"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = {
            "canceled_by": user.id,
            "canceled_at": datetime.now(),
            "canceled_reason": request.data.get("reason"),
            "leave_status": 6,  # status id Canceled
        }

        total_time = queryset.total_time
        employee = queryset.user_id
        leave_type = queryset.leave_type.HOOK_KEY
        check_status = queryset.authorizer_by
        request_date_year = queryset.end_date.year

        # LeaveSummaryController.calculate_leave_balance_cancel(employee, record_id, total_time, leave_type, request_date_year)
        # return False

        serializer = LeaveRequestCancelSerializer(
            instance=queryset, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()

            # re-calculate balance if record final approved
            if check_status is not None:
                LeaveSummaryController.calculate_leave_balance_cancel(
                    employee, record_id, total_time, leave_type, request_date_year
                )

            noti_message = f"have been canceled your leave request."
            # url = f"/admin/eleave/leave_summary"
            pk_encrypt = IdEncryption.encrypt_id(queryset.id)
            url = f"/admin/eleave/leave_summary/view/{pk_encrypt}"
            email_hook = f"ELEAVE_LEAVE_CANCEL"
            status_name = f"Canceled"

            LeaveSummaryController.send_notification(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                noti_message,
                url,
                queryset,
                status_name,
            )

            LeaveSummaryController.send_email(
                sender["user_id"],
                receiver["user_id"],
                queryset.id,
                module_data.id,
                url,
                email_hook,
                queryset,
                status_name,
            )

            return ApiResponse.success(
                message="Canceled successfully.",
                results=serializer.data,
            )
        return ApiResponse.error(errors=serializer.errors)

    @api_view(["GET"])
    def listing_status(request):
        queryset = LeaveRequestStatus.objects.all()
        serializer = LeaveRequestStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def send_notification_and_email(
        sender_user,
        receiver_users,
        record_id,
        module_id,
        noti_message,
        url,
        email_hook,
        instance,
        status_name,
    ):
        try:
            sender = GlobalHelper.find_user_info_by_user_id(sender_user)
            receiver = GlobalHelper.find_user_info_by_user_id(receiver_users)
            user_requestor = GlobalHelper.find_user_info_by_user_id(instance.user_id.id)
            data_notification = {
                "from_user": sender["user_id"],  # user requested
                "to_user": receiver["user_id"],  # to user by id
                "url": url,  # url click to access link route (insert your frontend route)
                "message": noti_message,  # message send to notification
                "record_id": record_id,  # recode id (input your primary key row data)
                "module_id": module_id,  # module id (input your moduleID)
                "is_read": False,  # unread
            }
            serializer_notification = NotificationStoreSerializer(
                data=data_notification
            )
            if serializer_notification.is_valid():
                serializer_notification.save()
                # increase unread notification by user
                unread_count = GlobalHelper.increase_user_unread_noti(
                    receiver["user_id"]
                )
                # message = unread_count  # return count unread to client
                message = {
                    "total_unread": unread_count,
                    "message": sender["full_name"] + " " + noti_message,
                }
                NotificationSending.send_notification_to_user(
                    receiver["user_id"], message
                )
                email_template = getEmailTemplateByHook(email_hook)
                leave_type = GlobalHelper.find_leave_type_by_id(instance.leave_type.id)
                template_title = email_template.title
                template_message = email_template.message
                total_time = float(instance.total_time) / 60
                message_body = {
                    "[FROM_USER]": sender["first_name"] + " " + sender["last_name"],
                    "[TO_USER]": receiver["first_name"] + " " + receiver["last_name"],
                    "[REQUESTOR]": user_requestor["first_name"]
                    + " "
                    + user_requestor["last_name"],
                    "[SITE_URL]": settings.DOMAIN_WEB + url,
                    "[SITE_NAME]": settings.SITE_NAME,
                    "[STATUS]": status_name,
                    "[LEAVE_TYPE]": str(leave_type.name),
                    "[FROM_DATE]": str(
                        datetime.strptime(
                            str(instance.start_date), "%Y-%m-%d"
                        ).strftime("%d-%m-%Y")
                    ),
                    "[TO_DATE]": str(
                        datetime.strptime(str(instance.end_date), "%Y-%m-%d").strftime(
                            "%d-%m-%Y"
                        )
                    ),
                    "[FROM_TIME]": str(instance.from_time),
                    "[TO_TIME]": str(instance.to_time),
                    "[TOTAL_TIME]": f"{str(round(total_time))}h",
                    "[REASON]": instance.reason,
                }
                user_template_message = template_message
                for keyword, replacement in message_body.items():
                    user_template_message = user_template_message.replace(
                        keyword, replacement
                    )
                send_email_inbound(
                    template_title, user_template_message, receiver["email"]
                )

        except ValidationError as e:
            ValidationError({e})

    @transaction.atomic
    def send_notification(
        sender_user,
        receiver_users,
        record_id,
        module_id,
        noti_message,
        url,
        instance,
        status_name,
    ):
        try:
            sender = GlobalHelper.find_user_info_by_user_id(sender_user)
            receiver = GlobalHelper.find_user_info_by_user_id(receiver_users)
            user_requestor = GlobalHelper.find_user_info_by_user_id(instance.user_id.id)
            data_notification = {
                "from_user": sender["user_id"],  # user requested
                "to_user": receiver["user_id"],  # to user by id
                "url": url,  # url click to access link route (insert your frontend route)
                "message": noti_message,  # message send to notification
                "record_id": record_id,  # recode id (input your primary key row data)
                "module_id": module_id,  # module id (input your moduleID)
                "is_read": False,  # unread
            }
            serializer_notification = NotificationStoreSerializer(
                data=data_notification
            )
            if serializer_notification.is_valid():
                serializer_notification.save()
                # increase unread notification by user
                unread_count = GlobalHelper.increase_user_unread_noti(
                    receiver["user_id"]
                )
                # message = unread_count  # return count unread to client
                message = {
                    "total_unread": unread_count,
                    "message": sender["full_name"] + " " + noti_message,
                }
                NotificationSending.send_notification_to_user(
                    receiver["user_id"], message
                )
        except ValidationError as e:
            ValidationError({e})

    def send_email(
        sender_user,
        receiver_users,
        record_id,
        module_id,
        url,
        email_hook,
        instance,
        status_name,
    ):
        # take info of users
        user_requestor = GlobalHelper.find_user_info_by_user_id(instance.user_id.id)
        sender = GlobalHelper.find_user_info_by_user_id(sender_user)
        receiver = GlobalHelper.find_user_info_by_user_id(receiver_users)
        # get email hook and template
        email_template = getEmailTemplateByHook(email_hook)
        template_title = email_template.title
        template_message = email_template.message
        # leave request instance info
        leave_type = GlobalHelper.find_leave_type_by_id(instance.leave_type.id)

        display_hour = None
        display_minute = None

        hour_int = int(instance.hours)
        minute_int = int(instance.minute)

        if hour_int > 0:
            display_hour = f"{hour_int} hour"

        if minute_int > 0:
            display_minute = f" {minute_int} minute"

        if display_hour is None:
            display_hour = ""

        if display_minute is None:
            display_minute = ""

        total_time = display_hour + display_minute

        message_body = {
            "[FROM_USER]": sender["full_name"],
            "[TO_USER]": receiver["full_name"],
            "[REQUESTOR]": user_requestor["full_name"],
            "[SITE_URL]": settings.DOMAIN_WEB + url,
            "[SITE_NAME]": settings.SITE_NAME,
            "[STATUS]": status_name,
            "[LEAVE_TYPE]": str(leave_type.name),
            "[FROM_DATE]": str(
                datetime.strptime(str(instance.start_date), "%Y-%m-%d").strftime(
                    "%d-%m-%Y"
                )
            ),
            "[TO_DATE]": str(
                datetime.strptime(str(instance.end_date), "%Y-%m-%d").strftime(
                    "%d-%m-%Y"
                )
            ),
            "[FROM_TIME]": str(instance.from_time),
            "[TO_TIME]": str(instance.to_time),
            "[TOTAL_TIME]": total_time,
            "[REASON]": instance.reason,
        }
        user_template_message = template_message
        for keyword, replacement in message_body.items():
            user_template_message = user_template_message.replace(keyword, replacement)
        send_email_inbound(template_title, user_template_message, receiver["email"])

    @staticmethod
    def get_staff_gender(user_id):
        try:
            info = User.objects.filter(id=user_id).first()
            return info.gender
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_leave_type(id):
        try:
            info = LeaveTypeModel.objects.filter(id=id).first()
            return info.name
        except LeaveTypeModel.DoesNotExist:
            return None

    @staticmethod
    def get_leave_status(id):
        try:
            info = LeaveRequestStatus.objects.filter(id=id).first()
            return info.name
        except LeaveRequestStatus.DoesNotExist:
            return None

    @staticmethod
    def get_current_annual_leave_by_hour(user_id):
        try:
            queryset = (
                LeaveBalance.objects.filter(employee=user_id).order_by("-year").first()
            )
            if queryset is not None:
                current_annual_leave = queryset.current_annual_leave / 60
                return round(current_annual_leave, 2)
            else:
                return None
        except LeaveBalance.DoesNotExist:
            return None

    @staticmethod
    def get_encrypt_key(id):
        if not id:
            return None
        return IdEncryption.encrypt_id(id)

    @staticmethod
    def get_leave_files(leave_id):
        try:
            leave_files = LeaveFile.objects.filter(leave_id=leave_id)
            serializer = LeaveFileSerializer(leave_files, many=True)
            return serializer.data
        except LeaveFile.DoesNotExist:
            return None
