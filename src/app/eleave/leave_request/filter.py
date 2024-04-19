from django_filters import rest_framework as filters
from .models import LeaveRequest


class LeaveRequestFilter(filters.FilterSet):
	class Meta:
		model = LeaveRequest
		fields = (
			"id",
			"staff_id",
			"staff_name"
		)
