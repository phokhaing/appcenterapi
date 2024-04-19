from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils import timezone
from .filter import LeaveTypeFilter
from .serializer import LeaveTypeSerializer
from .models import LeaveTypeModel

from ...utils.UserAccessPermission import permission_required


module_name = "ELEAVE/LEAVE_TYPE"


class LeaveTypePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class LeaveTypeController(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = LeaveTypeModel.objects.all()
    serializer_class = LeaveTypeSerializer
    pagination_class = LeaveTypePagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = ("id", "name", "acronym", "deduct_days_off", "created_by", "created_at")
    ordering_fields = fields  # ordering by field name
    search_fields = [
      'id',
      'name',
      'acronym',

   ]  # search by field name  
    filterset_class = LeaveTypeFilter
    # GET USERS 
    def perform_create(self, serializer):
      
      serializer.save(created_by=self.request.user, created_at=timezone.now())

    # @permission_required(module_name, "LIST")
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @permission_required(module_name, "CREATE")
    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

    # @permission_required(module_name, "UPDATE")
    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

    # @permission_required(module_name, "VIEW")
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)

    # @permission_required(module_name, "DELETE")
    # def destroy(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)


class LeaveTypeListing(APIView):
    def get(self, request):
        queryset = LeaveTypeModel.objects.all()
        serializer = LeaveTypeSerializer(queryset, many=True)
        return Response(serializer.data)
