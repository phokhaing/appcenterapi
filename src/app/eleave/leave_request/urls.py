from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
	LeaveRequestViewSet,
	FetchUserCertifyAuthorize,
	list_data_default_form,
	list_leave_reason
)

router = DefaultRouter()
router.register("", viewset=LeaveRequestViewSet, basename="leave_request")

urlpatterns = \
	[
    path('view/<str:pk>/', LeaveRequestViewSet.view_leave_request, name='view_leave_request'),
		path("get_user_certify_and_authorize/", FetchUserCertifyAuthorize.as_view(), name="get_user_certify_and_authorize"),
		path("list_data_default_form/", list_data_default_form, name="list_data_default_form"),
		path("list_leave_reason/", list_leave_reason, name="list_leave_reason"),
		path("listing/leave_request/", LeaveRequestViewSet.listing_leave_request, name="listing_leave_request"),
		path("listing/filter_export_leave_request/", LeaveRequestViewSet.filter_export_leave_request, name="filter_export_leave_request"),
	] + router.urls
