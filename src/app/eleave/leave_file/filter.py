from django_filters import rest_framework as filters
from .models import LeaveFile,


class LeaveFileFilter(filters.FilterSet):
	class Meta:
		model = LeaveFile
		fields = (
			"id",
			"leave_id",
			"upload_file_name",
			"original_name"
		)
