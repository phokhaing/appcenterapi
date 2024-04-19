from rest_framework import serializers

from ..models import Module, ModulePermission
from .permission import PermissionSerializer


class ModuleSerializer(serializers.ModelSerializer):
   # permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)
   permissions = PermissionSerializer(many=True, read_only=True)

   class Meta:
      model = Module
      fields = ('id', 'module_name', 'path', 'status', 'permissions')


class ModulePermissionSerializer(serializers.ModelSerializer):
   permission = PermissionSerializer()

   class Meta:
      model = ModulePermission
      fields = ['id', 'module_id', 'permission_id', 'permission']