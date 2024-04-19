from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, MenuOrderableViewSet
from .views import MenuNavbarListingApiView, MenuCustomDeleteApiView, UpdateMenuItemApiView

router = DefaultRouter()

router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'menu-orderable', MenuOrderableViewSet, basename='menu-orderable')

urlpatterns = [
    path('', include(router.urls)),
    path('menu_navbar_listing/', MenuNavbarListingApiView.as_view(), name='menu_navbar_listing'),
    path('menu_custom_delete/<str:menu_ids>/', MenuCustomDeleteApiView.as_view(), name='menu_custom_delete'),
    path('custom_update/<int:pk>/', UpdateMenuItemApiView.as_view(), name='menu_custom_update'),

]