from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import HolidayModel,WeekendModel
from import_export.admin import ImportExportModelAdmin



class HolidayAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = [
        "id", 
        "date", 
        "type", 
        "title", 
        "default_leave_contract",
        "created_by",
        "updated_by"]

    list_display_links = [
      "id", 
      "date", 
      "type", 
      "title", 
      "default_leave_contract",
      "created_by",
      "updated_by"]
    
    search_fields = [
      "date", 
      "type", 
      "title", 
      "default_leave_contract",
      "created_by",
      "updated_by"
    ]
admin.site.register(HolidayModel,HolidayAdmin)


class WeekendAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = [
        "id", 
        "title", 
        "days", 
        "year", 
        "mark_as",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "default_leave_contract"]
    list_display_links = [
        "id", 
        "title", 
        "days", 
        "year", 
        "mark_as",
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
        "default_leave_contract"]
    search_fields = ['year', 'title', 'days','default_leave_contract']
    
admin.site.register(WeekendModel,WeekendAdmin)


