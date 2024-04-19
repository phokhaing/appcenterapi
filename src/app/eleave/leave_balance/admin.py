from django.contrib import admin

from .models import LeaveBalance

from import_export.admin import ImportExportModelAdmin


class LeaveBalanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = [
        "id",
        "employee",
        "start_date",
        "end_date",
        "year",
        "entitle_balance",
        "additional_balance",
        "forward_balance",
        "begin_annual_leave",
        "taken_annual_leave",
        "current_annual_leave",
        "begin_sick_leave",
        "taken_sick_leave",
        "current_sick_leave",
        "begin_special_leave",
        "taken_special_leave",
        "current_special_leave",
        "begin_maternity_leave",
        "taken_maternity_leave",
        "current_maternity_leave",
        "begin_unpaid_Leave",
        "taken_unpaid_leave",
        "current_unpaid_leave",
        "created_by",
        "created_at",
    ]

    list_display_links = ["employee", "id"]
    search_fields = ["employee__username", "start_date", "end_date"]


admin.site.register(LeaveBalance, LeaveBalanceAdmin)
