from django.urls import path
from .views import LeaveContractController, ListingLeaveContract

urlpatterns = [
    path("", LeaveContractController.list_leave_contract),
    path("create", LeaveContractController.create_leave_contract),
    path(
        "view/<int:pk>/",
        LeaveContractController.view_leave_contract,
        name="view_leave_contract",
    ),
    path(
        "update/<int:pk>/",
        LeaveContractController.update_leave_contract,
        name="update_leave_contract",
    ),
    path(
        "delete/<int:pk>/",
        LeaveContractController.delete_leave_contract,
        name="delete_leave_contract",
    ),
    path(
        "listing_leave_contract",
        ListingLeaveContract.as_view(),
        name="listing_leave_contract",
    ),
]
