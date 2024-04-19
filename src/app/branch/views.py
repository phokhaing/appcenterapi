#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : PHO KHAING                                     |
#  | EMAIL: khaing.pho1991@gmail.com                       |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Full-Stack Software Developer                  |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import DjangoObjectPermissions

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import BranchFilter
from .models import Branch
from .serializer import BranchSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

from ..utils.UserAccessPermission import permission_required

module_name = "SETTING/BRANCH"


class BranchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


"""
# @author: soydara168@gmail.com
# @param: 08/June/2023
# @param: method for crud branch module
"""


class BranchController(viewsets.ModelViewSet):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [DjangoObjectPermissions]

    serializer_class = BranchSerializer
    queryset = Branch.objects.all()
    pagination_class = BranchPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)

    fields = (
        "code",
        "name_en",
        "name_kh",
        "address_en",
        "address_kh",
        "description",
        "is_active",
    )
    ordering_fields = fields  # ordering by field name
    search_fields = fields  # search by field name
    filterset_class = BranchFilter  # filter by field name

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


class BranchListing(APIView):
    def get(self, request):
        queryset = Branch.objects.all()
        serializer = BranchSerializer(queryset, many=True)
        return Response(serializer.data)
