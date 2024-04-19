from rest_framework.routers import DefaultRouter
from .views import RoleController
from rest_framework import viewsets

router = DefaultRouter()
router.register("", viewset=RoleController, basename="role")
urlpatterns = router.urls
