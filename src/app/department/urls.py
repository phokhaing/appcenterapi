from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DepartmentController, DepartmentListing
from rest_framework import viewsets

router = DefaultRouter()
router.register('', viewset=DepartmentController, basename='department')
# urlpatterns = router.urls
urlpatterns = [
                 path("department-listing/", DepartmentListing.as_view(), name="department-listing"),
              ] + router.urls
