#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : SOY DARA                                       |
#  | EMAIL: soydara168@gmail.com                           |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  | ROLE : Software Developer                             |
#  +-------------------------------------------------------+
#  | Released 13.3.2023.                                   |
#  +-------------------------------------------------------+

from django.urls import path

from .views import LeaveSummaryController

urlpatterns = [
    path("listing/leave_request/by_user/", LeaveSummaryController.listing_leave_request_by_user, name="listing_leave_request_by_user"),
    path("listing/leave_approval/by_user/", LeaveSummaryController.listing_leave_approval_by_user, name="listing_leave_approval_by_user"),
    path("listing/leave_balance/by_user/", LeaveSummaryController.listing_leave_balance_by_user, name="listing_leave_balance_by_user"),
    path("certifier/authorize/by_user/<int:record_id>/", LeaveSummaryController.certifier_authorize_by_user, name="certifier_authorize_by_user"),
    path("approve/authorize/by_user/<int:record_id>/", LeaveSummaryController.approve_authorize_by_user, name="approve_authorize_by_user"),
    path("reject/authorize/by_user/<int:record_id>/", LeaveSummaryController.reject_authorize_by_user, name="reject_authorize_by_user"),
    path("cancel/authorize/by_user/<int:record_id>/", LeaveSummaryController.cancel_authorize_by_user, name="cancel_authorize_by_user"),
    path("listing_status/", LeaveSummaryController.listing_status, name="listing_status"),
]