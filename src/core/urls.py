from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib import admin
from django.urls import path, include

# eLeave Urls
# from app.eleave.admin import eleave_admin_site
from app.eleave.leave_type.urls import urlpatterns as leave_type_urls
from app.eleave.leave_contract.urls import urlpatterns as leave_contract_urls
from app.eleave.leave_reason.urls import urlpatterns as leave_reason_urls
from app.eleave.holiday.urls import urlpatterns as holiday_urls


# config swegger ui
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# import api_urls
from rest_framework import permissions
from app.user_management.views import CustomAuthToken, MyTokenObtainPairView
from app.user_management.views.user import ForgotPasswordView

# point image location
from django.conf import settings
from django.conf.urls.static import static

from decouple import config

domain_name = config("DOMAIN_NAME")
# from user_management.views import Us
site_title = "FTB SUPPORTDESK API"
schema_view = get_schema_view(
    openapi.Info(
        title=site_title,
        default_version="v1",
        description="FTB BANK SYSTEM",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="khaing.pho1991@gmail.com"),
        license=openapi.License(name="FTB License"),
    ),
    public=True,
    permission_classes=[permissions.IsAdminUser],
    url=f"{domain_name}",
)

# JWT Config

# router = DefaultRouter()
# router.register('', api_urls)

admin.site.site_header = site_title  # default: "Django Administration"
# admin.site.index_title = 'Features area' # default: "Site administration"
admin.site.site_title = "FTB API"  # default: "Django site admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    # swegger route
    # path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    # path("redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path(
    #     "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    # ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # API Route
    # /rest-auth/login
    # path('rest-auth/', include('rest_auth.urls')),
    # path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # rest_framework route
    path("api/v1/auth/", include("rest_framework.urls")),
    path("api/v1/auth/login/", CustomAuthToken.as_view(), name="login"),
    path(
        "api/v1/auth/forgot_password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    # django_rest_auth
    # path('api/v1/rest-auth/', include('rest_auth.urls')),
    # django-allauth
    # path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    # allauth route
    # auth/account_login, account_logout, account_set_password
    # path('api/v1/auth/', include('allauth.urls')),
    # auth/ signup/ [name='account_signup']
    # auth/ login/ [name='account_login']
    # auth/ logout/ [name='account_logout']
    # auth/ password/change/ [name='account_change_password']
    # auth/ password/set/ [name='account_set_password']
    # auth/ inactive/ [name='account_inactive']
    # auth/ email/ [name='account_email']
    # auth/ confirm-email/ [name='account_email_verification_sent']
    # auth/ ^confirm-email/(?P<key>[-:\w]+)/$ [name='account_confirm_email']
    # auth/ password/reset/ [name='account_reset_password']
    # auth/ password/reset/done/ [name='account_reset_password_done']
    # auth/ ^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$ [name='account_reset_password_from_key']
    # auth/ password/reset/key/done/ [name='account_reset_password_from_key_done']
    # jwt route
    # path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # default
    path(
        "api/v1/auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),  # custom
    path(
        "api/v1/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("api/v1/auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # auth route
    # path('api/v1/auth/login/', CustomAuthToken.as_view(), name="login"),
    path("api/v1/user/", include("app.user_management.urls")),
    # path('api/v1/appraisal/', include('app.appraisal.urls')),
    # Apps routes
    path("api/v1/branch/", include("app.branch.urls")),
    path("api/v1/department/", include("app.department.urls")),
    path("api/v1/position/", include("app.position.urls")),
    # E-leave route
    # path("eleave_admin/", include(eleave_admin_site.urls)),
    path("api/v1/eleave/leave_type/", include(leave_type_urls)),
    path("api/v1/eleave/leave_contract/", include(leave_contract_urls)),
    path("api/v1/eleave/leave_reason/", include(leave_reason_urls)),
    path("api/v1/eleave/leave_request/", include("app.eleave.leave_request.urls")),
    path("api/v1/eleave/leave_summary/", include("app.eleave.leave_summary.urls")),
    path("api/v1/eleave/leave_balance/", include("app.eleave.leave_balance.urls")),
    path("api/v1/eleave/holiday/", include(holiday_urls)),
    path("api/v1/user_notification/", include("app.user_notification.urls")),
    path("", include("django_prometheus.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
