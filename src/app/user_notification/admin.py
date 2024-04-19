from django.contrib import admin
from .models import Notification, EmailHook, EmailLanguage, EmailTemplate
from import_export.admin import ImportExportModelAdmin

@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   list_display = ['from_user',
                   'to_user',
                   'url',
                   'message',
                   'module_id',
                   'is_read',
                   'created_at']

   list_display_links = ["from_user", "to_user", "url"]

   def from_user_username(self, obj):
      return obj.from_user.username

   from_user_username.short_description = 'From User'

@admin.register(EmailHook)
class EmailHookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   list_display = ['hook',
                   'hook_name',
                   'created_by',
                   'updated_by',
                   'created_at',
                   'updated_at',
                   'status']

   list_display_links = ["hook", "hook_name", "status", "created_by", "updated_by", "created_at", "updated_at"]
   search_fields = ['hook_name', 'hook']


@admin.register(EmailLanguage)
class EmailLanguageAdmin(admin.ModelAdmin):
   list_display = ['title',
                   'created_by',
                   'updated_by',
                   'created_at',
                   'updated_at',
                   'status']

   list_display_links = ["title", "status", "created_by", "updated_by", "created_at", "updated_at"]
   search_fields = ['title']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   list_display = ['title',
                   'message',
                   'hook',
                   'language',
                   'created_by',
                   'updated_by',
                   'created_at',
                   'updated_at',
                   'status']

   list_display_links = ["title", "message", "hook", "language", "status", "created_by", "updated_by", "created_at", "updated_at"]
   search_fields = ['title']
