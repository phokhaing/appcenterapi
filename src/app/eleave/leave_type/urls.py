from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LeaveTypeController, LeaveTypeListing
from rest_framework import viewsets

router = DefaultRouter()
router.register("", viewset=LeaveTypeController, basename="leave_type")
# urlpatterns = router.urls
urlpatterns = [
    path("leave_type_listing/", LeaveTypeListing.as_view(), name="leave_type_listing"),
] + router.urls
