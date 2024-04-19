from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Branch

class BranchAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['id',
                    'code',
                    'name_en',
                    'name_kh',
                    'address_en',
                    'is_active']

    list_display_links = ["id", "name_en", "name_kh"]

admin.site.register(Branch, BranchAdmin)