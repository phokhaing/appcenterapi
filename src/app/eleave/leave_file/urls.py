from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LeaveFileViewSet

router = DefaultRouter()
router.register("", viewset=LeaveFileViewSet, basename="leave_file")

urlpatterns = [
] + router.urls
