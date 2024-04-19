from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Position


class PositionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "name_en", "name_kh", "segment", "description", "is_active"]
    list_display_links = ["id", "name_en", "name_kh"]

admin.site.register(Position, PositionAdmin)