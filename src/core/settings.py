from datetime import timedelta
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_NAME = "App Center"


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "django-insecure-*q$r4#8q4*$3qbi^6^-h3rs=u2c4hafj&d(8b=g8wq_a9%h1mo"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

PROJECT_APPS = [
    "app.user_management.apps.UserManagementConfig",
    "app.appraisal.apps.AppraisalConfig",
    "app.branch.apps.BranchConfig",
    "app.department.apps.DepartmentConfig",
    "app.position.apps.PositionConfig",
    "app.menu.apps.MenuConfig",
    "app.user_notification.apps.UserNotificationConfig",
    # E-leave system
    "app.eleave.apps.EleaveConfig",  # main directory
    "app.eleave.leave_type.apps.LeaveTypeConfig",
    "app.eleave.leave_request.apps.LeaveRequestConfig",
    "app.eleave.leave_contract.apps.LeaveContractConfig",
    "app.eleave.leave_file.apps.LeaveFileConfig",
    "app.eleave.holiday.apps.HolidayConfig",
    "app.eleave.leave_summary.apps.LeaveSummaryConfig",
    "app.eleave.leave_balance.apps.LeaveBalanceConfig",
    "app.eleave.leave_reason.apps.LeaveReasonConfig",
]

DJANGO_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    "django_prometheus",
]

THIRD_PARTY_APPS = [
    # djangorestframework
    "rest_framework",
    #    'django.contrib.sites',
    "corsheaders",
    # django_rest_auth
    # Token Authentication
    "rest_framework.authtoken",
    "django_filters",
    # 'rest_auth',
    # Swegger
    "drf_yasg",
    # django-allauth
    # 'allauth',
    # 'allauth.account',
    # 'rest_auth.registration',
    # config django-allauth login with social, google, facebook, github ...
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    # jwt
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "channels",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    # All your other middlewares go here, including the default
    # middlewares like SessionMiddleware, CommonMiddleware,
    # CsrfViewmiddleware, SecurityMiddleware, etc.
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

# configure override user
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # 'rest_framework.authentication.BasicAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        # this one is allow access by provide token key
        # 'rest_framework.authentication.TokenAuthentication',
        # jwt
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "USER_DETAILS_SERIALIZER": "user_management.serializer.UserDetailsSerializer",
    # https://django-filter.readthedocs.io/en/stable/guide/tips.html
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.static",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.sqlite3",
    #     "NAME": "ftb_supportdesk_db",
    # }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql",
    #     "NAME": "ftb_supportdesk_db",
    #     "USER": "postgres",
    #     "PASSWORD": "postgres",
    #     "HOST": "192.168.2.3",
    #     "PORT": "5432",
    # }
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Phnom_Penh"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static")
# ]

# location upload file
MEDIA_URL = "/file_storage/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/file_storage")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
GET_MEDIA_URL = f"{config('DOMAIN_NAME')}/file_storage"
DOMAIN_NAME = f"{config('DOMAIN_NAME')}"
DOMAIN_WEB = f"{config('DOMAIN_WEB')}"
# Set the maximum size (in bytes) that a request's body may be
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10 MB
# Set the maximum size (in bytes) that a file may be before it is streamed to the file system
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10 MB

print("--------------- domain name ---------------------")
print(DOMAIN_NAME)

# Allow client site access api
# ref: https://github.com/adamchainz/django-cors-headers#configuration
# CORS_ALLOW_ALL_ORIGINS = True # allow access from any site
# CSRF_TRUSTED_ORIGINS = ["https://dev.api.appcenter.ftb.com.kh"]

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())
# ALLOWALL for Frontend can view/read file using embed or iframe because default it set 'X-Frame-Options' to 'deny'
X_FRAME_OPTIONS = "ALLOWALL"  # Default DENY


# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",  # ftb_supportdesk_web
# ]

ACCOUNT_EMAIL_VERIFICATION = "none"
# ACCOUNT_AUTHENTICATION_METHOD (=”username” | “email” | “username_email”)
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = False
AUTH_USER_MODEL = "user_management.User"

# ******* JWT Config ******
SIMPLE_JWT = {
    # "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1440),  # 24 hours
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# ****** Email Configuration ******** #
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Email account 1 (inbound)
EMAIL_HOST_1 = config("EMAIL_HOST_1")
EMAIL_PORT_1 = config("EMAIL_PORT_1", cast=int)
EMAIL_HOST_USER_1 = config("EMAIL_HOST_USER_1")
EMAIL_HOST_PASSWORD_1 = config("EMAIL_HOST_PASSWORD_1")
EMAIL_USE_SSL_1 = config("EMAIL_USE_SSL_1", default=True, cast=bool)
EMAIL_USE_TLS_1 = config("EMAIL_USE_TLS_1", default=True, cast=bool)
DEFAULT_FROM_EMAIL_1 = EMAIL_HOST_USER_1

# Email account 2 (outbound)
EMAIL_HOST_2 = config("EMAIL_HOST_2")
EMAIL_PORT_2 = config("EMAIL_PORT_2", cast=int)
EMAIL_HOST_USER_2 = config("EMAIL_HOST_USER_2")
EMAIL_HOST_PASSWORD_2 = config("EMAIL_HOST_PASSWORD_2")
EMAIL_USE_SSL_2 = config("EMAIL_USE_SSL_2", default=True, cast=bool)
EMAIL_USE_TLS_2 = config("EMAIL_USE_TLS_2", default=True, cast=bool)
DEFAULT_FROM_EMAIL_2 = EMAIL_HOST_USER_2

# # ****** Email Credentials Configs FTB ******** #
#  email1 = noreply.appcenter@ftb.com.kh
#  email2 = appcenter@ftb.com.kh
#  pass   = ftb12345$
#  Port   = 25

# Default to using Email account 1 settings
EMAIL_HOST = EMAIL_HOST_1
EMAIL_PORT = EMAIL_PORT_1
EMAIL_USE_TLS = EMAIL_USE_TLS_1
EMAIL_USE_SSL = EMAIL_USE_SSL_1
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL_1

ASGI_APPLICATION = "core.asgi.application"

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# ----------------------------------------------------------
# SSL Certificate for Django and run HTTPS
# ----------------------------------------------------------
# Set the secure proxy SSL header (for reverse proxy setups)
# CSRF_TRUSTED_ORIGINS = [
#     "https://dev.api.appcenter.ftb.com.kh",
#     "https://dev.appcenter.ftb.com.kh",
#     "http://192.168.106.110:3000",
# ]

# use below for https
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# USE_X_FORWARDED_PORT = True
# SWAGGER_SETTINGS = {
#     "DEFAULT_SCHEME": "https",
#     # ... other settings
# }

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
