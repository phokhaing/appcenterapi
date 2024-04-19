from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import Q

from ..models import Role, Module, RoleModule, Permission, ModulePermission
from ..serializer import (
    RoleSerializer,
    ModuleSerializer,
    RoleModuleSerializer,
    PermissionSerializer,
)
from ..filter import RoleFilter

from django.utils.decorators import method_decorator

from ..serializer.role import RoleModuleCustomSerializer
from ...utils.UserAccessPermission import permission_required

from ...utils.global_paginator import PaginatorResponse
from ...utils.global_api_response import ApiResponse
from django.http import Http404

module_name = "SETTING/ROLE"


class NoPagination(PageNumberPagination):
    page_size = None


class RolePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class RoleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = RolePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    fields = (
        "id",
        "role_name_en",
        "role_name_kh",
        "description",
        "is_active",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # search by field name
    filterset_class = RoleFilter

    @permission_required(module_name, "LIST")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_name, "CREATE")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class RoleRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @permission_required(module_name, "VIEW")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class RoleUpdateAPIView(generics.UpdateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @permission_required(module_name, "UPDATE")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class RoleDestroyAPIView(generics.DestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @permission_required(module_name, "DELETE")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


# list data no Pagination
class RoleListingApiView(APIView):
    @permission_required(module_name, "LIST")
    def get(self, request):
        queryset = Role.objects.all()
        serializer = RoleSerializer(queryset, many=True)
        return Response(serializer.data)


class ListModuleByRoleIDAPIView(APIView):
    def get(self, request, role_id):
        filter = request.GET.get("filter")
        queryset = RoleModule.objects.filter(role_id=role_id).order_by("-created_at")

        if filter is not None and filter == "a_z":
            queryset = queryset.filter(role_id=role_id).order_by("module__module_name")

        if filter is not None and filter == "z_a":
            queryset = queryset.filter(role_id=role_id).order_by("-module__module_name")

        search_fields = ["module__module_name"]
        filter_fields = ["module__module_name"]

        paginator = PaginatorResponse(
            queryset=queryset,
            request=request,
            serializer_class=RoleModuleCustomSerializer,
            search_fields=search_fields,
            filter_fields=filter_fields,
            page_size=request.GET.get("page_size", 10),
        )

        return ApiResponse.success(
            message="Role module retrieved successfully",
            results=paginator.paginator_results(),
            paginators=paginator.api_response_paginators(),
            count=paginator.paginator_count(),
            next=paginator.paginator_next(),
            previous=paginator.paginator_previous(),
        )

    # def get(self, request, role_id):
    #    try:
    #       role = Role.objects.get(pk=role_id)
    #       role_modules = role.modules.all()
    #
    #       module_permissions = ModulePermission.objects.filter(role=role, module__in=role_modules)
    #
    #       module_ids = role_modules.values_list('id', flat=True)
    #       modules = Module.objects.filter(id__in=module_ids)
    #
    #       data = []
    #       for module in modules:
    #          module_data = {
    #             'id': RoleModule.objects.get(role=role, module=module).id,  # Add the id field from ftb_role_modules
    #             'module_id': module.id,
    #             'role_id': role_id,
    #             'module_name': module.module_name,
    #             'permissions': module_permissions.filter(module=module).values_list('permission__permission_name',
    #                                                                                 flat=True)
    #          }
    #          data.append(module_data)
    #
    #       return Response(data, status=status.HTTP_200_OK)
    #    except Role.DoesNotExist:
    #       return Response({"message": "Role not found."}, status=status.HTTP_404_NOT_FOUND)


# list module not existing by role id
class ListModuleNotExistingByRoleIDAPIView(APIView):
    @permission_required(module_name, "LIST")
    def get(self, request, role_id):
        try:
            role = Role.objects.get(id=role_id)
            modules = Module.objects.exclude(roles=role)
            serializer = ModuleSerializer(modules, many=True)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response(
                {"message": "Module not found."}, status=status.HTTP_404_NOT_FOUND
            )


# save module to role
class SaveModuleToRoleAPIView(APIView):
    @permission_required(module_name, "CREATE")
    def post(self, request):
        module_ids = request.data.get(
            "module_id", []
        )  # Retrieve module IDs from the request data
        role_id = request.data.get("role_id")  # Retrieve role ID from the request data

        try:
            role = Role.objects.get(id=role_id)  # Get the role instance
            # Add the new module associations
            role.modules.add(*module_ids)

            return Response(
                {"message": "Modules saved to role successfully"},
                status=status.HTTP_200_OK,
            )
        except Role.DoesNotExist:
            return Response(
                {"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND
            )


class DeleteModuleToRoleAPIView(APIView):
    @permission_required(module_name, "DELETE")
    def delete(self, request, row_id, module_id, role_id):
        try:
            queryset_role_module = get_object_or_404(
                RoleModule, pk=row_id, module=module_id, role=role_id
            )
            queryset_role_module.delete()
            queryset_module_permission = ModulePermission.objects.filter(
                role=role_id, module=module_id
            )
            queryset_module_permission.delete()

            return Response(
                {"message": "Module permissions deleted successfully."}, status=200
            )

        except RoleModule.DoesNotExist:
            return Response(
                {"message": "No RoleModule matches the given query."}, status=404
            )
