from rest_framework import serializers
from .models import Menu, MenuOrderable
from ..user_management.models import Module

from ..user_management.serializer import ModuleSerializer
import json


class MenuSerializer(serializers.ModelSerializer):
   class Meta:
      model = Menu
      fields = ('id', 'menu_name_en', 'menu_name_kh', 'menu_icon', 'module_url')


class MenuOrderableSerializer(serializers.ModelSerializer):
   orderable = serializers.SerializerMethodField()

   def get_orderable(self, instance):
      orderable = instance.orderable
      if isinstance(orderable, str):
         orderable = json.loads(orderable)
      return orderable

   def process_children(self, items, module_mapping):
      children = []
      for item in items:
         module_id = item['module_url']
         module = module_mapping.get(module_id)
         if module:
            item['module_url'] = ModuleSerializer(module).data
         children.append(item)
      return children

   # def to_representation(self, instance):
   # 	representation = super().to_representation(instance)
   # 	orderable = representation.get('orderable', [])
   #
   # 	module_ids = [item['module_url'] for item in orderable if item['module_url']]
   # 	modules = Module.objects.filter(id__in=module_ids)
   # 	module_mapping = {module.id: module for module in modules}
   #
   # 	representation['orderable'] = self.process_children(orderable, module_mapping)
   #
   # 	return representation
   def to_representation(self, instance):
      representation = super().to_representation(instance)
      orderable = representation.get('orderable', [])

      # Create a list of module_url ids from the orderable list
      module_ids = [item['module_url']['id'] if isinstance(item['module_url'], dict) else item['module_url']
                    for item in orderable]

      # Replace the 'module_url' values with just the id
      for item in orderable:
         if isinstance(item['module_url'], dict):
            item['module_url'] = item['module_url']['id']

      # Update the 'orderable' list in the representation
      representation['orderable'] = orderable

      return representation

   class Meta:
      model = MenuOrderable
      fields = '__all__'


class ModuleCustomSerializer(serializers.ModelSerializer):
   class Meta:
      model = Module
      fields = ('id', 'module_name', 'path')


class MenuCustomSerializer(serializers.ModelSerializer):
   module_url = serializers.SerializerMethodField()

   class Meta:
      model = Menu
      fields = ('id', 'menu_name_en', 'menu_name_kh', 'menu_icon', 'module_url')

   def get_module_url(self, obj):
      module_url = obj.module_url
      if module_url:
         try:
            module = Module.objects.get(pk=int(module_url))
            serializer = ModuleCustomSerializer(module)
            return serializer.data
         except (ValueError, Module.DoesNotExist):
            pass
      return None


class MenuOrderableSaveSerializer(serializers.ModelSerializer):
   class Meta:
      model = MenuOrderable
      fields = '__all__'
