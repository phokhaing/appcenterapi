from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoObjectPermissions

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import LeaveBalanceFilter
from .models import LeaveBalance
from .serializer import LeaveBalanceSerializer, LeaveBalanceFetchOneSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from ...utils.UserAccessPermission import permission_api_view_required
from django.utils import timezone
import datetime

module_name = "ELEAVE/LEAVE_BALANCE"


@api_view(["GET"])
@permission_api_view_required(module_name, "LIST")
def list_leave_balances(request):
    page_size = request.GET.get("page_size")
    paginator = PageNumberPagination()
    if page_size:
        paginator.page_size = page_size
    leave_balances = LeaveBalance.objects.all().order_by("-created_at")

    user_id = request.GET.get("user_id")
    if user_id:
        leave_balances = leave_balances.filter(Q(employee=user_id))

    department = request.GET.get("department")
    if department is not None:
        leave_balances = leave_balances.filter(employee__department_id=department)

    branch = request.GET.get("branch")
    if branch is not None:
        leave_balances = leave_balances.filter(employee__branch_id=branch)

    from_year = request.GET.get("from_year")
    if from_year is not None:
        from_date_year = datetime.datetime.strptime(from_year, "%Y")
        leave_balances = leave_balances.filter(year__gte=from_date_year.year)

    to_year = request.GET.get("to_year")
    if to_year is not None:
        to_date_year = datetime.datetime.strptime(to_year, "%Y")
        leave_balances = leave_balances.filter(year__lte=to_date_year.year)

    search_query = request.GET.get("search", "")
    if search_query:
        leave_balances = leave_balances.filter(
            Q(employee__username__icontains=search_query)
            | Q(employee__staff_id__icontains=search_query)
        )

    context = paginator.paginate_queryset(leave_balances, request)
    serializer = LeaveBalanceSerializer(context, many=True)
    paginated_response = paginator.get_paginated_response(serializer.data)
    serialized_data = paginated_response.data
    return Response(
        {
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "List Leave Balance",
            "count": serialized_data["count"],
            "next": serialized_data["next"],
            "results": serialized_data["results"],
        }
    )


@api_view(["POST"])
@permission_api_view_required(module_name, "CREATE")
def create_leave_balance(request):
    data = request.data
    importedData = data.get("importedData")

    if importedData is None:
        # Handle single create
        serializer = LeaveBalanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, created_at=timezone.now())
            return Response(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Leave Balance was created",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif isinstance(importedData, list):
        # Handle multi-create
        success_data = []  # To store successfully created leave balances
        error_data = []  # To store data with validation errors

        for data_item in importedData:
            serializer = LeaveBalanceSerializer(data=data_item)
            if serializer.is_valid():
                serializer.save(created_by=request.user, created_at=timezone.now())
                success_data.append(serializer.data)
            else:
                # Store data with validation errors
                error_data.append({"data": data_item, "errors": serializer.errors})

        # Check if any leave balances were created successfully
        if success_data:
            return Response(
                {
                    "success": True,
                    "status": status.HTTP_200_OK,
                    "message": "Leave Balances were created",
                    "data": success_data,
                }
            )

        # If no leave balances were created successfully, return validation errors
        return Response(
            {
                "success": False,
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Some leave balances could not be created due to validation errors",
                "errors": error_data,
            }
        )
    else:
        return Response(
            {"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_api_view_required(module_name, "VIEW")
def fetch_one_leave_balance(request, pk):
    try:
        leave_balance = LeaveBalance.objects.get(pk=pk)
    except LeaveBalance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LeaveBalanceFetchOneSerializer(leave_balance)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_api_view_required(module_name, "UPDATE")
def update_leave_balance(request, pk):
    try:
        leave_balance = LeaveBalance.objects.get(pk=pk)
    except LeaveBalance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

        # Set the user making the update
    request.data["updated_by"] = request.user.id

    serializer = LeaveBalanceSerializer(leave_balance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "Leave Balance was updated",
                "data": serializer.data,
            }
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_api_view_required(module_name, "DELETE")
def delete_leave_balance(request, pk):
    try:
        leave_balance = LeaveBalance.objects.get(pk=pk)
    except LeaveBalance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    leave_balance.delete()
    return Response(
        {
            "success": True,
            "status": status.HTTP_204_NO_CONTENT,
            "message": "Leave Balance was Deleted",
        }
    )
