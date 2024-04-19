from django_filters import rest_framework as filters
from ..models import Module


class ModuleFilter(filters.FilterSet):

   class Meta:
      model = Module

      fields = (
         "id",
         "module_name",
         "path"
      )