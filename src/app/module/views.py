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

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import DjangoObjectPermissions

from .filter import BranchFilter
from .models import Branch
from .serializer import BranchSerializer


class BranchController(viewsets.ModelViewSet):
   authentication_classes = [TokenAuthentication]
   # permission_classes = [DjangoObjectPermissions]
   
   serializer_class = BranchSerializer
   queryset = Branch.objects.all()
   
   filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
   
   fields = (
      "code",
      "name_en",
      "name_kh",
      "address_en",
      "address_kh",
      "description",
      "is_active"
   )
   ordering_fields = fields  # ordering by field name
   search_fields = fields  # search by field name
   filterset_class = BranchFilter  # filter by field name
   
   # filterset_fields = {
   #    'id'     : ["in", "exact"],  # used /?id__in=2
   #    'name_en': ["exact"]
   # }
   
   # def create(self, request, *args, **kwargs):
   # data = request.data['fname']
   
   # many = isinstance(data, list)
   # serializer = self.get_serializer(data=data, many=many)
   # serializer.is_valid(raise_exception=True)
   # self.perform_create(serializer)
