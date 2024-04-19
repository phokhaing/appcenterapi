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
from django import forms
from django.db import models
from django_filters import CharFilter, BooleanFilter
from django_filters import rest_framework as filters

from .models import Branch


class BranchFilter(filters.FilterSet):
   # add-on filtering fields
   # min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
   # max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
   
   # ChoiceFilter
   # category = django_filters.ModelChoiceFilter(
   #    field_name='category', lookup_expr='isnull',
   #    null_label='Uncategorized',
   #    queryset=Category.objects.all(),
   # )
   
   class Meta:
      model = Branch
      
      # option 1, filter by default (exact)
      fields = (
         "id",
         "code",
         "name_en",
         "name_kh",
         "address_en",
         "address_kh",
         "description",
         "is_active"
      )
      
      # option 2, filter by specific option given
      # fields = {
      #    'code'  : ['exact'],
      #    'name_en'  : ['exact', 'contains'],
      #    'last_login': ['exact', 'year__gt'],
      # }
      
      # override filter form
      # filter_overrides = {
      #    models.CharField   : {
      #       'filter_class': CharFilter,
      #       'extra'       : lambda f: {
      #          'lookup_expr': 'icontains',
      #       },
      #    },
      #    models.BooleanField: {
      #       'filter_class': BooleanFilter,
      #       'extra'       : lambda f: {
      #          'widget': forms.CheckboxInput,
      #       },
      #    },
      # }
