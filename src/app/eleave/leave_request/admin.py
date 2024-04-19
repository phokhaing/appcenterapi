from django.contrib import admin
from .models import LeaveRequest, LeaveRequestStatus
from import_export.admin import ImportExportModelAdmin


@admin.register(LeaveRequest)
class LeaveRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = [
		"id",
		"staff_id",
		"staff_name",
		"staff_position",
		"leave_status",
		"leave_type",
		"start_date",
		"total_time",
		"end_date",
		"requested_by",
		"requested_at",
		"certifier",
		"certifier_by",
		"certifier_at",
		"authorizer",
		"authorizer_by",
		"authorizer_at",
		"rejected_by",
		"rejected_at"
	]
	
	list_display_links = ["staff_id", "staff_name"]
	search_fields = ['staff_id', 'staff_name']
	list_filter = ('leave_type', 'leave_status', 'authorizer_by',)


@admin.register(LeaveRequestStatus)
class LeaveRequestStatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = [
		"id",
		"name",
		"created_by",
		"updated_by",
		"created_at",
		"updated_at",
	]
	
	list_display_links = ["name"]
	search_fields = ['name']
