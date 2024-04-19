from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BranchController, BranchListing
from rest_framework import viewsets

router = DefaultRouter()
router.register('', viewset=BranchController, basename='branch')
# urlpatterns = router.urls
urlpatterns = [
                 path("branch-listing/", BranchListing.as_view(), name="branch-listing"),
              ] + router.urls
