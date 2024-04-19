from rest_framework import serializers
from ..models import Role, RoleModule, Module, Permission, ModulePermission
from .module import ModuleSerializer


class RoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Role
		fields = "__all__"
		# depth = 1
	
	_length: int = 100
	
	def validate_role_name_en(self, value):
		if len(value) > self._length:
			raise serializers.ValidationError(
				f"Role name en can't greater then {self._length} characters."
			)
		return value
	
	def validate_role_name_kh(self, value):
		if len(value) > self._length:
			raise serializers.ValidationError(
				f"Role name kh can't greater then {self._length} characters."
			)
		return value


class RoleModuleSerializer(serializers.ModelSerializer):
	module = ModuleSerializer()
	
	class Meta:
		model = RoleModule
		fields = ['id', 'role_id', 'module_id', 'module']


class RoleModuleCustomSerializer(serializers.ModelSerializer):
	created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
	updated_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
	
	module_name = serializers.SerializerMethodField()
	permissions = serializers.SerializerMethodField()
	
	class Meta:
		model = RoleModule
		fields = ["id", "role", "module", "module_name", "permissions", "created_at", "created_by", "updated_at", "updated_by"]
	
	def get_module_name(self, obj):
		try:
			module_instance = obj.module
			return module_instance.module_name
		except Module.DoesNotExist:
			return None
	
	def get_permissions(self, obj):
		try:
			module_permissions = ModulePermission.objects.filter(role=obj.role, module=obj.module)
			return module_permissions.values_list('permission__permission_name', flat=True)
		except ModulePermission.DoesNotExist:
			return None