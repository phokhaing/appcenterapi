from drf_yasg import openapi
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .models import HolidayModel,WeekendModel
from .serializer import HolidaySerializer,WeekendSerializer
from .filter import HolidayFilter,WeekendFilther
# from .resources import WeekendResource
# from import_export.formats import base_formats

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.http import HttpResponse
from ...utils.UserAccessPermission import permission_required


module_holiday = "ELEAVE/HOLIDAY"

class HolidayPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class HolidayController(viewsets.ModelViewSet):
    queryset = HolidayModel.objects.all()
    serializer_class = HolidaySerializer
    pagination_class = HolidayPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    fields = ("id", "date", "type", "title", "default_leave_contract", "created_by", "updated_by","created_at", "updated_at")
    ordering_fields = fields  # ordering by field name
    search_fields = ("id", "date", "type")
    ordering_fields =  fields
    filterset_class = HolidayFilter
    # GET USERS CREATE
    def perform_create(self, serializer):
      serializer.save(created_by=self.request.user, created_at=timezone.now())
    # GET USERS UPDATE
    def perform_update(self, serializer):
      serializer.save(updated_by=self.request.user, updated_at=timezone.now())

    @permission_required(module_holiday, 'LIST')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_holiday, 'CREATE')
    def create(self, request, *args, **kwargs):
          return super().create(request, *args, **kwargs)

    @permission_required(module_holiday, 'UPDATE')
    def update(self, request, *args, **kwargs):
          return super().update(request, *args, **kwargs)

    @permission_required(module_holiday, 'VIEW')
    def retrieve(self, request, *args, **kwargs):
          return super().retrieve(request, *args, **kwargs)

    @permission_required(module_holiday, 'DELETE')
    def destroy(self, request, *args, **kwargs):
          return super().destroy(request, *args, **kwargs)

class HolidayListing(APIView):
    def get(self, request):
        queryset = HolidayModel.objects.all()
        serializer = HolidaySerializer(queryset, many=True)
        return Response(serializer.data)


class WeekendPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class WeekendController(viewsets.ModelViewSet):
    queryset = WeekendModel.objects.all()
    serializer_class = WeekendSerializer
    pagination_class = WeekendPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    fields = ("id", "title", "days", "year", "mark_as", "created_at", "created_by","updated_at", "updated_by","default_leave_contract")
    ordering_fields = ("title", "days", "year")  # ordering by field name
    search_fields = ("title", "days", "year")  # search by field name
    filterset_class = WeekendFilther
    # GET USERS CREATE
    def perform_create(self, serializer):
      serializer.save(created_by=self.request.user, created_at=timezone.now())
    # GET USERS UPDATE
    def perform_update(self, serializer):
      serializer.save(updated_by=self.request.user, updated_at=timezone.now())
    
    @permission_required(module_holiday, 'LIST')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_holiday, 'CREATE')
    def create(self, request, *args, **kwargs):
          return super().create(request, *args, **kwargs)

    @permission_required(module_holiday, 'UPDATE')
    def update(self, request, *args, **kwargs):
          return super().update(request, *args, **kwargs)

    @permission_required(module_holiday, 'VIEW')
    def retrieve(self, request, *args, **kwargs):
          return super().retrieve(request, *args, **kwargs)

    @permission_required(module_holiday, 'DELETE')
    def destroy(self, request, *args, **kwargs):
          return super().destroy(request, *args, **kwargs)
    
class WeekendListing(APIView):
    def get(self, request):
        queryset = WeekendModel.objects.all()
        serializer = WeekendSerializer(queryset, many=True)
        return Response(serializer.data)
    
