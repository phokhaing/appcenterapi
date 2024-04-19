#  +-------------------------------------------------------+
#  | NAME : PHO KHAING                                     |
#  | EMAIL: khaing.pho@ftb.com.kh                          |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 20.08.2023.                                  |
#  +-------------------------------------------------------+

from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import LeaveContractModel
from .serializer import LeaveContractSerializer

# Global Helpers
from ...utils.UserAccessPermission import permission_api_view_required
from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse
from ...utils.global_openapi_schema import (
    global_request_openapi_schema,
    global_response_openapi_shema,
)
from django.utils import timezone


module_name = "ELEAVE/LEAVE_CONTRACT"


class LeaveContractController:
    # ----------------------------------------------------------------
    # @author: Pho Khaing
    # @date  : 19-08-2023
    # @method: list data by pagination, filter, search of contract
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="GET",
        operation_description="Retrieve a list of contracts with pagination, search and filtering",
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
    @api_view(["GET"])
    @permission_api_view_required(module_name, "LIST")
    def list_leave_contract(request):
        search_fields = ["name", "status"]
        filter_fields = ["name", "status"]
        queryset = LeaveContractModel.objects.order_by("-created_at")

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=LeaveContractSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="Leave contracts list retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    # ----------------------------------------------------------------
    # @author: Pho Khaing
    # @date  : 19-08-2023
    # @method: view contract data by id
    # ----------------------------------------------------------------

    @api_view(["GET"])
    @permission_api_view_required(module_name, "VIEW")
    def view_leave_contract(request, pk):
        try:
            queryset = LeaveContractModel.objects.get(pk=pk)
            serializer = LeaveContractSerializer(queryset)

            return ApiResponse.success(
                message="Leave contract retrieved successfully.",
                results=serializer.data,
            )
        except LeaveContractModel.DoesNotExist:
            return ApiResponse.not_found()

    # ----------------------------------------------------------------
    # @author: Pho Khaing
    # @date  : 19-08-2023
    # @method: create new contract data
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="POST",
        operation_description="Create a new leave contract",
        request_body=global_request_openapi_schema(LeaveContractSerializer),
        responses=global_response_openapi_shema(LeaveContractSerializer),
    )
    @api_view(["POST"])
    @permission_api_view_required(module_name, "CREATE")
    def create_leave_contract(request):
        serializer = LeaveContractSerializer(data=request.data)
        if serializer.is_valid():
            # Assuming request.user is a User instance
            serializer.validated_data["created_by"] = request.user
            serializer.validated_data["created_at"] = timezone.now()
            serializer.save()
            return ApiResponse.created(
                message="Leave contract created successfully.",
                results=serializer.data,
            )

        return ApiResponse.error(errors=serializer.errors)

    # ----------------------------------------------------------------
    # @author: Pho Khaing
    # @date  : 19-08-2023
    # @method: update contract data by id
    # ----------------------------------------------------------------
    @swagger_auto_schema(
        method="PUT",
        operation_description="Update an existing leave contract by id",
        request_body=global_request_openapi_schema(LeaveContractSerializer),
        responses=global_response_openapi_shema(LeaveContractSerializer),
    )
    @api_view(["PUT"])
    @permission_api_view_required(module_name, "UPDATE")
    def update_leave_contract(request, pk):
        try:
            queryset = LeaveContractModel.objects.get(pk=pk)
        except LeaveContractModel.DoesNotExist:
            return ApiResponse.not_found()
        if request.method == "PUT":
            serializer = LeaveContractSerializer(queryset, data=request.data)
            if serializer.is_valid():
                # Assuming request.user is a User instance
                serializer.validated_data["updated_by"] = request.user
                serializer.validated_data["updated_at"] = timezone.now()
                serializer.save()
                return ApiResponse.success(
                    message="Leave contract updated successfully.",
                    results=serializer.data,
                )

        return ApiResponse.error(errors=serializer.errors)

    # ----------------------------------------------------------------
    # @author: Pho Khaing
    # @date  : 19-08-2023
    # @method: delete contract data by id
    # ----------------------------------------------------------------
    @api_view(["DELETE"])
    @permission_api_view_required(module_name, "DELETE")
    def delete_leave_contract(request, pk):
        try:
            queryset = LeaveContractModel.objects.get(pk=pk)
            queryset.delete()
            return ApiResponse.no_content(
                message="Leave contract deleted successfully."
            )

        except LeaveContractModel.DoesNotExist:
            return ApiResponse.not_found()


class ListingLeaveContract(APIView):
    def get(self, request):
        queryset = LeaveContractModel.objects.all()
        serializer = LeaveContractSerializer(queryset, many=True)

        # Customize the response format
        data = {
            "success": True,
            "status": 200,
            "message": "Leave contracts list retrieved successfully",
            "results": serializer.data,
        }

        return Response(data)
