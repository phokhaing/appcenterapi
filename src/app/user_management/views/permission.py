from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Permission
from ..serializer import PermissionSerializer
from ..filter import PermissionFilter

from django.utils.decorators import method_decorator
from ...utils.UserAccessPermission import permission_required

module_name = 'SETTING/PERMISSION'


class NoPagination(PageNumberPagination):
   page_size = None


class PermissionPagination(PageNumberPagination):
   page_size = 10
   page_size_query_param = "page_size"


class PermissionListCreateAPIView(generics.ListCreateAPIView):
   queryset = Permission.objects.all()
   serializer_class = PermissionSerializer
   pagination_class = PermissionPagination
   filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
   fields = ("permission_name", "is_active")
   ordering_fields = fields  # ordering by field name
   search_fields = fields  # search by field name
   filterset_class = PermissionFilter

   @permission_required(module_name, 'LIST')
   def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

   @permission_required(module_name, 'CREATE')
   def create(self, request, *args, **kwargs):
      return super().create(request, *args, **kwargs)


class PermissionRetrieveAPIView(generics.RetrieveAPIView):
   queryset = Permission.objects.all()
   serializer_class = PermissionSerializer

   @permission_required(module_name, 'VIEW')
   def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)


class PermissionUpdateAPIView(generics.UpdateAPIView):
   queryset = Permission.objects.all()
   serializer_class = PermissionSerializer

   @permission_required(module_name, 'UPDATE')
   def update(self, request, *args, **kwargs):
      return super().update(request, *args, **kwargs)


class PermissionDestroyAPIView(generics.DestroyAPIView):
   queryset = Permission.objects.all()
   serializer_class = PermissionSerializer

   @permission_required(module_name, 'DELETE')
   def destroy(self, request, *args, **kwargs):
      return super().destroy(request, *args, **kwargs)


# list data no Pagination
class PermissionListingApiView(APIView):
   @permission_required(module_name, 'LIST')
   def get(self, request):
      queryset = Permission.objects.all()
      serializer = PermissionSerializer(queryset, many=True)
      return Response(serializer.data)
