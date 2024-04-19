from django.shortcuts import render
from rest_framework import viewsets, pagination
from .models import Menu, MenuOrderable
from ..user_management.models import Module
from .serializer import MenuSerializer, MenuOrderableSerializer, MenuCustomSerializer, MenuOrderableSaveSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from django.http import JsonResponse
from ..utils.UserAccessPermission import permission_required
from django.shortcuts import get_object_or_404

module_name = 'SETTING/MENU'
from django.http import Http404
from django.db import transaction
from rest_framework.exceptions import ValidationError


class NoPagination(pagination.PageNumberPagination):
   page_size = None


# route for form submit save
class MenuViewSet(viewsets.ViewSet):
   @permission_required(module_name, 'CREATE')
   @transaction.atomic
   def create(self, request):
      try:
         # insert get id django
         serializer = MenuSerializer(data=request.data)
         serializer.is_valid(raise_exception=True)
         model_instance = serializer.save()
         inserted_record_id = model_instance.id
         # get data by id
         get_data = Menu.objects.get(id=inserted_record_id)
         serializer = MenuSerializer(get_data)
         data = {
            'id': serializer.data['id'],
            'menu_name_en': serializer.data['menu_name_en'],
            'menu_name_kh': serializer.data['menu_name_kh'],
            'menu_icon': serializer.data['menu_icon'],
            'module_url': serializer.data['module_url']
         }
         # Convert single object to a list json
         json_menu_data = data
         # get data menu_orderable
         menu_orderable = MenuOrderable.objects.first()
         if menu_orderable is None:
            context_menu_item_default = {
               'orderable': '[]'
            }
            serializer = MenuOrderableSaveSerializer(data=context_menu_item_default)
            if serializer.is_valid():
               item_default = serializer.save()
            # retrieve the saved instance
            menu_orderable = serializer.instance
         # convert data to json
         json_orderable_data = json.loads(menu_orderable.orderable)
         # Include json1 into json2
         json_orderable_data.append(json_menu_data)
         # convert json data format, single quotes (') to double quotes (")
         json_orderable_data_str = json.dumps(json_orderable_data)
         # save data after merge json by first with field name
         menu_orderable.orderable = json_orderable_data_str
         menu_orderable.save()

         return Response({'message': 'success', 'data': json_orderable_data}, status=status.HTTP_201_CREATED)
      except ValidationError as e:
         ValidationError({e})

   # @permission_required(module_name, 'CREATE')
   # @transaction.atomic
   # def create(self, request):
   #    try:
   #       # insert get id django
   #       serializer = MenuSerializer(data=request.data)
   #       serializer.is_valid(raise_exception=True)
   #       model_instance = serializer.save()
   #       inserted_record_id = model_instance.id
   #
   #       # get data by id
   #       get_data = Menu.objects.get(id=inserted_record_id)
   #       serializer = MenuSerializer(get_data)
   #
   #       data = {
   #          'id': serializer.data['id'],
   #          'menu_name_en': serializer.data['menu_name_en'],
   #          'menu_name_kh': serializer.data['menu_name_kh'],
   #          'menu_icon': serializer.data['menu_icon'],
   #          'module_url': serializer.data['module_url']
   #       }
   #
   #       # Convert single object to a list json
   #       json_menu_data = data
   #
   #       # get data menu_orderable
   #       menu_orderable = MenuOrderable.objects.first()
   #       if menu_orderable is None:
   #          context_menu_item_default = {
   #             'orderable': '[]'
   #          }
   #          serializer = MenuOrderableSaveSerializer(data=context_menu_item_default)
   #          if serializer.is_valid():
   #             item_default = serializer.save()
   #       # convert data to json
   #       json_orderable_data = json.loads(menu_orderable.orderable)
   #
   #       # Include json1 into json2
   #       json_orderable_data.append(json_menu_data)
   #
   #       # convert json data format, single quotes (') to double quotes (")
   #       json_orderable_data_str = json.dumps(json_orderable_data)
   #
   #       # save data after merch json by first with field name
   #       menu_orderable.orderable = json_orderable_data_str
   #       menu_orderable.save()
   #
   #       return Response({'message': 'success', 'data': json_orderable_data}, status=status.HTTP_201_CREATED)
   #    except ValidationError as e:
   #       ValidationError({e})

   @permission_required(module_name, 'LIST')
   def list(self, request, *args, **kwargs):
      return super().list(request, *args, **kwargs)

   @permission_required(module_name, 'VIEW')
   def retrieve(self, request, pk=None):
      menu = get_object_or_404(Menu, id=pk)
      menu_serializers = MenuCustomSerializer(menu)
      return Response(menu_serializers.data, status=status.HTTP_200_OK)

   @permission_required(module_name, 'UPDATE')
   def update(self, request, *args, **kwargs):
      return super().update(request, *args, **kwargs)


# route update menu orderable for after drap drop
class MenuOrderableViewSet(viewsets.ModelViewSet):
   pagination_class = None
   queryset = MenuOrderable.objects.all()
   serializer_class = MenuOrderableSerializer

   @permission_required(module_name, 'UPDATE')
   def update(self, request, *args, **kwargs):
      data = request.data
      parsed_data = json.dumps(data)
      menu_orderable = MenuOrderable.objects.get(id=1)
      menu_orderable.orderable = parsed_data
      menu_orderable.save()

      return Response({'message': 'Data updated successfully'}, status=status.HTTP_201_CREATED)

   @permission_required(module_name, 'DELETE')
   def destroy(self, request, *args, **kwargs):
      instance = self.get_object()

      return Response({'message': 'Data deleted successfully', 'data': instance}, status=status.HTTP_204_NO_CONTENT)

   def list(self, request, *args, **kwargs):
      queryset = self.get_queryset()
      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data)

   @permission_required(module_name, 'VIEW')
   def retrieve(self, request, *args, **kwargs):
      return super().retrieve(request, *args, **kwargs)

   @permission_required(module_name, 'CREATE')
   def create(self, request, *args, **kwargs):
      return super().create(request, *args, **kwargs)


# list menu to frontend navigation
class MenuNavbarListingApiView(APIView):
   def get(self, request, *args, **kwargs):
      user = request.user

      menu_orderable = MenuOrderable.objects.first()
      json_data = json.loads(menu_orderable.orderable)

      def filter_item(item):
         module_url = item.get("module_url")
         if module_url and module_url != "":
            try:
               module_id = int(module_url)
               modules = Module.objects.filter(roles__users=user, id=module_id)
               if modules.exists():
                  module = modules.first()
                  item['module_url'] = {
                     "module_name": module.module_name,
                     "path": module.path
                  }
               else:
                  # If the user doesn't have access to the module, remove the item
                  return False
            except (ValueError, Module.DoesNotExist):
               pass

         children = item.get("children")
         if children:
            item['children'] = [child_item for child_item in children if filter_item(child_item)]
            # If all children are filtered out, remove the item as well
            if not item['children']:
               return False

         return True

      json_data = [item for item in json_data if filter_item(item)]

      return Response(json_data)


class MenuCustomDeleteApiView(APIView):
   @permission_required(module_name, 'DELETE')
   def delete(self, request, menu_ids, *args, **kwargs):
      menu_ids = menu_ids.split(',')  # Split the menu_ids string into a list of individual menu IDs

      try:
         Menu.objects.filter(id__in=menu_ids).delete()  # Delete menu items by IDs

         return JsonResponse({'message': 'Menu items deleted successfully', 'ids': menu_ids})
      except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)


class UpdateMenuItemApiView(APIView):
   def put(self, request, pk=None, format=None):
      data = request.data

      try:
         menu_orderable = MenuOrderable.objects.get(id=1)
      except MenuOrderable.DoesNotExist:
         raise Http404("MenuOrderable instance not found")

      updated_orderable = json.loads(menu_orderable.orderable)

      # Update the specific menu item in the orderable list based on id
      self.update_menu_item(updated_orderable, str(pk), data)

      # Save the updated orderable list as JSON
      menu_orderable.orderable = json.dumps(updated_orderable)
      menu_orderable.save()

      # Update the corresponding Menu model
      try:
         menu_item = Menu.objects.get(pk=pk)
      except Menu.DoesNotExist:
         raise Http404("Menu instance not found")

      menu_item.menu_name_en = data.get('menu_name_en')
      menu_item.menu_name_kh = data.get('menu_name_kh')
      menu_item.menu_icon = data.get('menu_icon')
      menu_item.module_url = data.get('module_url')
      menu_item.save()

      return Response({"message": "MenuOrderable and Menu updated successfully"})

   def update_menu_item(self, items, target_id, updated_data):
      for item in items:
         if str(item['id']) == target_id:
            item.update(updated_data)
            break
         if 'children' in item:
            self.update_menu_item(item['children'], target_id, updated_data)
