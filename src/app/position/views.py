from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from .filter import PositionFilter
from .serializer import PositionSerializer
from .models import Position

from ..utils.UserAccessPermission import permission_required

module_name = "SETTING/POSITION"


class PositionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


"""
# @author: soydara168@gmail.com
# @param: 08/June/2023
# @param: method for crud position module
"""


class PositionController(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = PositionPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = (
        "id",
        "name_en",
        "name_kh",
        "segment",
        "description",
        "is_active",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # Search by field name
    filterset_class = PositionFilter

    @permission_required(module_name, "LIST")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_name, "CREATE")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required(module_name, "UPDATE")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(module_name, "VIEW")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @permission_required(module_name, "DELETE")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PositionListing(APIView):
    def get(self, request):
        queryset = Position.objects.all()
        serializer = PositionSerializer(queryset, many=True)
        return Response(serializer.data)
