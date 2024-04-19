from django.urls import path, re_path
from .views import LeaveReasonController

urlpatterns = [
    path("", LeaveReasonController.list_leave_reason),
    path("create", LeaveReasonController.create_leave_reason),
    re_path(
        r"^view/(?P<pk>[0-9a-f-]+)/$",
        LeaveReasonController.view_leave_reason,
        name="view_leave_reason",
    ),
    re_path(
        r"^update/(?P<pk>[0-9a-f-]+)/$",
        LeaveReasonController.update_leave_reason,
        name="update_leave_reason",
    ),
    re_path(
        r"^delete/(?P<pk>[0-9a-f-]+)/$",
        LeaveReasonController.delete_leave_reason,
        name="delete_leave_reason",
    ),
]
