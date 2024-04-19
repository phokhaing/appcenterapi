from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import WeekendController, HolidayController, HolidayListing, WeekendListing


router = DefaultRouter()
router.register('dayoff' , viewset=HolidayController, basename="dayoff")
router.register('weekend' , viewset=WeekendController, basename="weekend")
# router.register('weekendexcel', viewset=WeekendController,basename="weekendexcel" )
urlpatterns = [
    path("holiday_listing/", HolidayListing.as_view, name="holiday_listing"),
    path("weekend_listing/", WeekendListing.as_view, name="weekend_listing"),
    # path("weekend_export/", ExportExcelView.as_view, name="weekend_export")
] + router.urls