from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import PositionController, PositionListing
from rest_framework import viewsets

router = DefaultRouter()
router.register('', viewset=PositionController, basename='position')
# urlpatterns = router.urls
urlpatterns = [
                 path("position-listing/", PositionListing.as_view(), name="position-listing"),
              ] + router.urls
