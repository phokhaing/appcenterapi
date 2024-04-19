from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from ..models import Module, ModulePermission, Permission, RoleModule, Role
from ..serializer import ModuleSerializer, ModulePermissionSerializer, PermissionSerializer
from ..filter import ModuleFilter
from ...utils.UserAccessPermission import permission_required

module_name = 'SETTING/MODULE'


class NoPagination(PageNumberPagination):
   page_size = None


class ModulePagination(PageNumberPagination):
   page_size = 10
   page_size_query_param = "page_size"


class ModuleListCreateAPIView(generics.ListCreateAPIView):
   queryset = Module.objects.all()
   serializer_class = ModuleSerializer
   pagination_class = ModulePagination
   filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
   fields = ("module_name", "path", "status")
   ordering_fields = fields
   search_fields = fields
   filterset_class = ModuleFilter

   @permission_required(module_name, 'CREATE')
   def create(self, request, *args, **kwargs):
      return super().create(request, *args, **kwargs)


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
   queryset = Module.objects.all()
   serializer_class = ModuleSerializer

   @permission_required(module_name, 'VIEW')
   def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)


class ModuleUpdateAPIView(generics.UpdateAPIView):
   queryset = Module.objects.all()
   serializer_class = ModuleSerializer

   @permission_required(module_name, 'UPDATE')
   def update(self, request, *args, **kwargs):
      return super().update(request, *args, **kwargs)


class ModuleDestroyAPIView(generics.DestroyAPIView):
   queryset = Module.objects.all()
   serializer_class = ModuleSerializer

   @permission_required(module_name, 'DELETE')
   def destroy(self, request, *args, **kwargs):
      return super().destroy(request, *args, **kwargs)


# list data no Pagination
class ModuleListingApiView(APIView):
   def get(self, request):
      queryset = Module.objects.all()
      serializer = ModuleSerializer(queryset, many=True)
      return Response(serializer.data)


# list permission by module id
class ListPermissionByModuleIDAPIView(APIView):
   # @permission_required(module_name, 'LIST')
   def get(self, request, role_id, module_id):
      try:
         module_permissions = ModulePermission.objects.filter(role_id=role_id, module_id=module_id).order_by('id')
         serializer = ModulePermissionSerializer(module_permissions, many=True)  # Serialize the queryset
         return Response(serializer.data, status=status.HTTP_200_OK)
      except Module.DoesNotExist:
         return Response({"message": "Module not found."}, status=status.HTTP_404_NOT_FOUND)


# list permission not existing by module id
class ListPermissionNotExistingByModuleIDAPIView(APIView):
   # @permission_required(module_name, 'LIST')
   def get(self, request, role_id, module_id):
      try:
         role_modules = RoleModule.objects.filter(role_id=role_id, module_id=module_id)
         existing_permissions = ModulePermission.objects.filter(role_id=role_id, module_id=module_id)

         permissions = Permission.objects.exclude(modulepermission__in=existing_permissions)
         permission_data = permissions.values('id', 'permission_name')

         return Response(permission_data)
      except Module.DoesNotExist:
         return Response({"message": "Module not found."}, status=status.HTTP_404_NOT_FOUND)


class SavePermissionToModuleAPIView(APIView):
   @permission_required(module_name, 'CREATE')
   def post(self, request):
      permission_ids = request.data.get('permission_id', [])  # Retrieve permission IDs from the request data
      module_id = request.data.get('module_id')  # Retrieve module ID from the request data
      role_id = request.data.get('role_id')  # Retrieve role ID from the request data

      try:
         module = Module.objects.get(id=module_id)
      except Module.DoesNotExist:
         return Response({"error": "Module not found"}, status=status.HTTP_404_NOT_FOUND)

      try:
         role = Role.objects.get(id=role_id)
      except Role.DoesNotExist:
         return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

      for permission_id in permission_ids:
         try:
            permission = Permission.objects.get(id=permission_id)
            module_permission = ModulePermission(role=role, module=module, permission=permission)
            module_permission.save()
         except Permission.DoesNotExist:
            return Response({"error": f"Permission with ID {permission_id} not found"},
                            status=status.HTTP_404_NOT_FOUND)

      return Response({"message": "Permissions saved to module successfully"}, status=status.HTTP_200_OK)


class DeletePermissionToModuleAPIView(APIView):
   @permission_required(module_name, 'DELETE')
   def delete(self, request, pk):
      with connection.cursor() as cursor:
         cursor.execute("DELETE FROM ftb_module_permissions WHERE id = %s", [pk])
      return Response({"message": "Row deleted successfully."}, status=status.HTTP_200_OK)
