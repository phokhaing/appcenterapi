# eleave/urls.py
from django.contrib import admin
from django.urls import path
from .admin import eleave_admin_site

urlpatterns = [
    path('eleave_admin/', eleave_admin_site.urls),
]
