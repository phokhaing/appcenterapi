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
from .models import Position


class PositionFilter(filters.FilterSet):
    class Meta:
        model = Position
        fields = (
            "id",
            "name_en",
            "name_kh",
            "segment",
            "description",
            "is_active",
        )
