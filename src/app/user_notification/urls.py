from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    EmailAPIView,
    EmailHookView,
    EmailLanguageView,
    EmailTemplateView,
    NotificationAPIView,
    TotalUserNotiAPIView,
    ListUnreadUserNotiAPIView,
    ListAllUserNotiAPIView,
    ViewNotiByUserAPIView,
    MakeReadAllByUserNotiAPIView,
    OptionSelectUserListingViewSet,
)

from .routing import websocket_urlpatterns

router = DefaultRouter()
router.register(r"email_hook", viewset=EmailHookView, basename="email_hook")
router.register(r"email_language", viewset=EmailLanguageView, basename="email_language")
router.register(r"email_template", viewset=EmailTemplateView, basename="email_template")

router.register(r"notification", viewset=NotificationAPIView, basename="notification")
# router.register(r'notification/by/user', viewset=ListAllUserNotiAPIView, basename="list-all-noti-by-user")

router.register(r"notification", viewset=NotificationAPIView, basename="notification")

router.register(
    "option_select_user_listing",
    viewset=OptionSelectUserListingViewSet,
    basename="option_select_user_listing",
)

urlpatterns = [
    path("send-email/", EmailAPIView.as_view(), name="send-email"),
    path(
        "total/unread/noti/by/user/",
        TotalUserNotiAPIView.as_view(),
        name="total-noti-by-user",
    ),
    path(
        "list/unread/noti/by/user/",
        ListUnreadUserNotiAPIView.as_view(),
        name="list-unread-noti-by-user",
    ),
    path(
        "notification/by/user/",
        ListAllUserNotiAPIView.as_view(),
        name="list-notifications",
    ),
    path(
        "notification/view/unread/noti/by/user/<int:pk>/",
        ViewNotiByUserAPIView.as_view(),
        name="view_noti_by-user",
    ),
    path(
        "make/all_read/noti/by/user/",
        MakeReadAllByUserNotiAPIView.as_view(),
        name="make_all_read_noti_by_user/",
    ),
    # websocket route
    path("ws/", include(websocket_urlpatterns)),
] + router.urls
