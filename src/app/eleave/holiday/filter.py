from django_filters import rest_framework as filters
from .models import HolidayModel,WeekendModel


class HolidayFilter(filters.FilterSet):
    class Meta:
        model = HolidayModel
        fields = (
            "id",
            "date",
            "type",
            "title",
            "default_leave_contract",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at"
        )

class WeekendFilther(filters.FilterSet):
    class Meta:
        model = WeekendModel
        fields = [
        "id", 
        "title", 
        "days", 
        "year", 
        "mark_as",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "default_leave_contract"]
