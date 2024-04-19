from rest_framework.routers import DefaultRouter
from .views import BranchController
from rest_framework import viewsets

router = DefaultRouter()
router.register('', viewset=BranchController, basename='branch')
urlpatterns = router.urls
