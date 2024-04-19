# from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin

# from .leave_contract.models import LeaveContractModel
# from .leave_reason.models import LeaveReasonModel
# from .leave_balance.models import LeaveBalance
# from .leave_request.models import LeaveRequest, LeaveRequestStatus
# from .leave_type.models import LeaveTypeModel


# # eleave/admin.py
# from django.contrib.admin import AdminSite
# from django.utils.translation import gettext_lazy as _


# class EleaveAdminSite(AdminSite):
#     site_header = _("ELEAVE MENU")


# admin.site = EleaveAdminSite(name="eleave")


# # Leave Contract Admin
# class LeaveContractAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "day_start",
#         "month_start",
#         "default_leave_type",
#         "created_by",
#         "updated_by",
#         "created_at",
#         "updated_at",
#         "status",
#     ]

#     list_display_links = ["id", "name"]


# admin.site.register(LeaveContractModel, LeaveContractAdmin)


# # Leave Balance Admin
# class LeaveBalanceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "employee",
#         "start_date",
#         "end_date",
#         "year",
#         "entitle_balance",
#         "additional_balance",
#         "forward_balance",
#         "begin_annual_leave",
#         "taken_annual_leave",
#         "current_annual_leave",
#         "begin_sick_leave",
#         "taken_sick_leave",
#         "current_sick_leave",
#         "begin_special_leave",
#         "taken_special_leave",
#         "current_special_leave",
#         "begin_maternity_leave",
#         "taken_maternity_leave",
#         "current_maternity_leave",
#         "begin_unpaid_Leave",
#         "taken_unpaid_leave",
#         "current_unpaid_leave",
#         "created_by",
#         "created_at",
#     ]

#     list_display_links = ["employee", "id"]
#     search_fields = ["employee__username", "start_date", "end_date"]


# admin.site.register(LeaveBalance, LeaveBalanceAdmin)


# # Leave Reason Admin
# class ReasonModelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "reason_en",
#         "reason_kh",
#         "created_by",
#         "updated_by",
#         "created_at",
#         "updated_at",
#         "status",
#     ]

#     list_display_links = ["id", "reason_en", "reason_kh"]


# admin.site.register(LeaveReasonModel, ReasonModelAdmin)


# # Leave Request
# @admin.register(LeaveRequest)
# class LeaveRequestAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "staff_id",
#         "staff_name",
#         "staff_position",
#         "leave_type",
#         "start_date",
#         "end_date",
#         "duration",
#         "requested_by",
#         "requested_at",
#         "certifier",
#         "certifier_by",
#         "certifier_at",
#         "authorizer",
#         "authorizer_by",
#         "authorizer_at",
#         "rejected_by",
#         "rejected_at",
#     ]

#     list_display_links = ["staff_id", "staff_name"]
#     search_fields = ["staff_id", "staff_name"]


# @admin.register(LeaveRequestStatus)
# class LeaveRequestStatusAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "created_by",
#         "updated_by",
#         "created_at",
#         "updated_at",
#     ]

#     list_display_links = ["name"]
#     search_fields = ["name"]


# # Leave Type
# class LeaveTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     list_display = [
#         "id",
#         "name",
#         "acronym",
#         "deduct_days_off",
#         "created_by",
#         "created_at",
#     ]

#     list_display_links = ["id", "name", "acronym"]
#     search_fields = [
#         "id",
#         "name",
#         "acronym",
#     ]


# admin.site.register(LeaveTypeModel, LeaveTypeAdmin)
