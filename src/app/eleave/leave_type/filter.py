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
from django_filters import rest_framework as filters
from .models import LeaveTypeModel


class LeaveTypeFilter(filters.FilterSet):
    class Meta:
        model = LeaveTypeModel
        fields = (
            "id",
            "name",
            "acronym",
            "deduct_days_off",
            "created_by"
        )
