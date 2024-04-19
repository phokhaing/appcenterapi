from drf_yasg import openapi
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .models import LeaveReasonModel
from .serializer import LeaveReasonSerializer

from rest_framework.exceptions import ValidationError

# Helper
from ...utils.UserAccessPermission import permission_api_view_required
from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse
from ...utils.global_openapi_schema import (
    global_request_openapi_schema,
    global_response_openapi_shema,
)
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status


module_name = "ELEAVE/LEAVE_REASON"


class LeaveReasonController:
    # ----------------------------------------------------------------
    # list data by pagination, filter, search of leave reasons
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="GET",
        operation_description="Retrieve a list of leave reasons with pagination, search, and filtering",
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
                name="name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by name",
                required=False,
            ),
            openapi.Parameter(
                name="status",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by status",
                required=False,
            ),
        ],
    )
    # ----------------------------------------------------------------
    # GET DATA TO LIST-ITEM
    # ----------------------------------------------------------------
    @api_view(['GET'])
    @permission_api_view_required(module_name, "LIST")
    def list_leave_reason(request):
        search_fields = ['reason_en', 'reason_kh', 'status']
        filter_fields = ["reason_en", 'reason_kh', 'status']
        queryset = LeaveReasonModel.objects.order_by("-created_at")

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=LeaveReasonSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get('page_size', 10),
        )

        return ApiResponse.success(
            message="Leave reason list retrieved successfully.",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    # ----------------------------------------------------------------
    # GET DATA TO VIEW
    # ----------------------------------------------------------------
    @api_view(["GET"])
    @permission_api_view_required(module_name, "VIEW")
    def view_leave_reason(request, pk):
        try:
            # Use get_object_or_404 with UUID primary key
            queryset = LeaveReasonModel.objects.get(id=pk)
            serializer = LeaveReasonSerializer(queryset)

            return ApiResponse.success(
                message="Leave reason retrieved successfully.",
                results=serializer.data,
            )
        except LeaveReasonModel.DoesNotExist:
            return ApiResponse.not_found()

    # ----------------------------------------------------------------
    # CREATE DATA
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="POST",
        operation_description="Create a new leave reason",
        request_body=global_request_openapi_schema(
            LeaveReasonSerializer),
        responses=global_response_openapi_shema(LeaveReasonSerializer),
    )
    @api_view(["POST"])
    @permission_api_view_required(module_name, "CREATE")
    def create_leave_reason(request):
        try:
            serializer = LeaveReasonSerializer(data=request.data)
            if serializer.is_valid():
                # Assuming request.user is a User instance
                serializer.validated_data["created_by"] = request.user
                serializer.validated_data["created_at"] = timezone.now()
                serializer.save()
                return ApiResponse.success(
                    message="Leave reason created successfully",
                    results=serializer.data,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # except PurchaseSettingModel.error:
        except ValidationError as e:
            return ApiResponse.error(errors=serializer.errors)

    # ----------------------------------------------------------------
    # UPDATE DATA
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="PUT",
        operation_description="Update leave reason",
        request_body=global_request_openapi_schema(
            LeaveReasonSerializer),
        responses=global_response_openapi_shema(LeaveReasonSerializer),
    )
    @api_view(["PUT"])
    @permission_api_view_required(module_name, "UPDATE")
    def update_leave_reason(request, pk):
        try:
            # Use get_object_or_404 with UUID primary key
            queryset = LeaveReasonModel.objects.get(id=pk)
        except LeaveReasonModel.DoesNotExist:
            return ApiResponse.not_found()
        try:
            if request.method == "PUT":
                serializer = LeaveReasonSerializer(
                    queryset, data=request.data)
                if serializer.is_valid():
                    # Assuming request.user is a User instance
                    serializer.validated_data["updated_by"] = request.user
                    serializer.validated_data["updated_at"] = timezone.now()
                    serializer.save()
                    return ApiResponse.success(
                        message="Leave reason updated successfully,",
                        results=serializer.data,
                    )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return ApiResponse.error(errors=serializer.errors, message=str(e.detail))
    # ----------------------------------------------------------------
    # DELETE DATA
    # ----------------------------------------------------------------

    @api_view(["DELETE"])
    @permission_api_view_required(module_name, "DELETE")
    def delete_leave_reason(request, pk):
        try:
            # Use get_object_or_404 with UUID primary key
            queryset = LeaveReasonModel.objects.get(id=pk)
            queryset.delete()
            return ApiResponse.no_content(
                message="Leave reason deleted successfully."
            )
        except LeaveReasonModel.DoesNotExist:
            return ApiResponse.not_found()
