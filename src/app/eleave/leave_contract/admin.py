from django.contrib import admin
from .models import LeaveContractModel

from import_export.admin import ImportExportModelAdmin


class LeaveContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ["id", "name", "day_start", "month_start", "default_leave_type", "created_by", "updated_by", "created_at", "updated_at", "status"]
	
	list_display_links = ["id", "name"]


admin.site.register(LeaveContractModel, LeaveContractAdmin)
