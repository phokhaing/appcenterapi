from django.contrib import admin

from .models import Appraisal, Template, Type


@admin.register(Appraisal)
class AppraisalAdmin(admin.ModelAdmin):
   list_display = ['id',
                   'template',
                   'appraisee',
                   'appraiser',
                   'active']


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
   list_display = ['id',
                   'title',
                   'type',
                   'active']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
   list_display = ['id',
                   'title',
                   'active']
