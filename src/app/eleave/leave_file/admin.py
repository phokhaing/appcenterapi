from django.contrib import admin
from .models import LeaveFile
from import_export.admin import ImportExportModelAdmin

@admin.register(LeaveFile)
class LeaveFileAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = [
		"id",
		"leave_id",
		"upload_file_name",
		"original_name",
		"file_type",
		"extension",
		"file_path",
	]
	
	list_display_links = ["leave_id", "upload_file_name", "original_name"]
	search_fields = ['leave_id', 'upload_file_name', 'original_name']
