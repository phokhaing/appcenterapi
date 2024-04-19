from django.contrib import admin
from .models import Role


@admin.register(Role)
class PositionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "role_name_en",
        "role_name_kh",
        "description",
        "is_active",
    ]

    list_display_links = ["id", "role_name_en"]
