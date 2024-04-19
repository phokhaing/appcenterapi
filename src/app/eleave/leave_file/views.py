from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .filter import LeaveFileFilter
from .serializer import LeaveFileSerializer
from .models import LeaveFile

from ...utils.UserAccessPermission import permission_required

module_name = "ELEAVE/LEAVE_FILE"


class LeaveFilePagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = "page_size"


class LeaveFileViewSet(viewsets.ModelViewSet):
	queryset = LeaveFile.objects.all()
	serializer_class = LeaveFileSerializer
	
	pagination_class = LeaveFilePagination
	filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
	
	fields = ("id", "leave_id", "upload_file_name", "original_name")
	ordering_fields = fields  # ordering by field name
	search_fields = fields  # search by field name
	filterset_class = LeaveFileFilter
	
	@permission_required(module_name, "LIST")
	def list(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "CREATE")
	def create(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "VIEW")
	def retrieve(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "UPDATE")
	def update(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "UPDATE")
	def partial_update(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "DELETE")
	def destroy(self, request, *args, **kwargs):
		return Response(status=405)
