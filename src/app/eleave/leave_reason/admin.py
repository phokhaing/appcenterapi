from django.contrib import admin
from .models import LeaveReasonModel
from import_export.admin import ImportExportModelAdmin


class ReasonModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
	list_display = ["id", "reason_en", "reason_kh", "created_by", "updated_by", "created_at", "updated_at", "status"]
	list_display_links = ["id", "reason_en", "reason_kh"]


admin.site.register(LeaveReasonModel, ReasonModelAdmin)
