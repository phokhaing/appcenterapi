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
from .models import LeaveContractModel


class LeaveContractFilter(filters.FilterSet):
    class Meta:
        model = LeaveContractModel
        fields = ("id", "name", "day_start", "month_start", "default_leave_type",
                  "created_by", "updated_by", "created_at", "updated_at")
