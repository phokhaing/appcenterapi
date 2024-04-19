from django.contrib import admin
from .models import Menu, MenuOrderable
from import_export.admin import ImportExportModelAdmin


@admin.register(Menu)
class MenuAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   list_display = ['id', 'menu_name_en', 'module_url']
   
   
@admin.register(MenuOrderable)
class MenuOrderableAdmin(ImportExportModelAdmin, admin.ModelAdmin):

   def has_add_permission(self, request):
      return False

   def has_change_permission(self, request, obj=None):
      return False

   def has_delete_permission(self, request, obj=None):
      return False

   list_display = ['id', 'orderable']

   list_display_links = ['id', 'orderable']
