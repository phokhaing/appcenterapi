from django_filters import rest_framework as filters
from .models import LeaveReasonModel


class TransportationTypeFilter(filters.FilterSet):
    class Meta:
        model = LeaveReasonModel
        fields = (
            "id",
            "reason_en",
            "reason_kh",
            "status",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at"
        )
