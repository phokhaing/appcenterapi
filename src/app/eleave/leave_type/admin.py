from django.contrib import admin
from .models import LeaveTypeModel

from import_export.admin import ImportExportModelAdmin


class LeaveTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = [
		"id",
		"name",
		"acronym",
		"deduct_days_off",
		"created_by",
		"created_at",
	]
	
	list_display_links = ["id", "name", "acronym"]
	search_fields = [
		"id",
		"name",
		"acronym",
	]


admin.site.register(LeaveTypeModel, LeaveTypeAdmin)
