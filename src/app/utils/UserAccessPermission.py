#  | NAME : SOY DARA                                             |
#  | EMAIL: soydara168@gmail.com                                 |
#  | PARAM : Manage user access depend on role module permission |
#  +-------------------------------------------------------------+
#  | Released 08.JUNE.2023.                                      |
#  | VERSION : V1                                                |
#  +-------------------------------------------------------------+
# from functools import wraps
# from django.http import JsonResponse, HttpResponseForbidden
# from ..user_management.models import ModulePermission, RoleModule, UserRole, Module
#
#
# def permission_required(module_name, permission_name):
#    def decorator(view_func):
#       @wraps(view_func)
#       def wrapped_view(self, request, *args, **kwargs):
#
#          user = request.user
#          if not user:
#             # User not found, deny access
#             return HttpResponseForbidden("User not found")
#
#          user_role = UserRole.objects.filter(user=user).first()
#          if not user_role:
#             # User role not found, deny access
#             return HttpResponseForbidden("User role not found")
#
#          module = Module.objects.filter(module_name=module_name).first()
#
#          if not module:
#             # Module not found, deny access
#             return HttpResponseForbidden("Module not found")
#
#          # Retrieve the module permission for the user's role
#          access = ModulePermission.objects.filter(
#             module=module,
#             permission__permission_name=permission_name,
#             role=user_role.role,
#          ).first()
#
#          if not access:
#             # Permission not found for the user's role, deny access
#             return HttpResponseForbidden("Access denied")
#          return view_func(self, request, *args, **kwargs)
#
#       return wrapped_view
#
#    return decorator


from ..user_management.models import ModulePermission, RoleModule, UserRole, Module

from functools import wraps
from django.http import HttpResponseForbidden


def permission_required(module_name, permission_name):
	def decorator(view_func):
		@wraps(view_func)
		def wrapped_view(self, request, *args, **kwargs):
			user = request.user
			if not user:
				# User not found, deny access
				return HttpResponseForbidden("User not found")
			
			module = Module.objects.filter(module_name=module_name).first()
			if not module:
				# Module not found, deny access
				return HttpResponseForbidden("Module not found")
			
			user_roles = user.roles.all()
			if not user_roles:
				# User has no roles, deny access
				return HttpResponseForbidden("User has no roles")
			
			# Retrieve the module permissions for the user's roles
			accesses = ModulePermission.objects.filter(
				module=module,
				permission__permission_name=permission_name,
				role__in=user_roles
			)
			
			if not accesses:
				# No permission found for any of the user's roles, deny access
				return HttpResponseForbidden("Access denied")
			
			# Permission found for at least one of the user's roles, grant access
			return view_func(self, request, *args, **kwargs)
		
		return wrapped_view
	
	return decorator


# +--------------------------------------------------+
# @param: Access control:
# @param: views.py
# @param: Apply on Viewset, ModelViewSet, Generic, Class-based, Function-based
# +--------------------------------------------------+
# Example
"""
    from ..utils.UserAccessPermission import permission_required
    module_name = 'POSITION' # Replace your module name

   @permission_required(module_name, 'LIST')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(module_name, 'CREATE')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required(module_name, 'UPDATE')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(module_name, 'VIEW')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @permission_required(module_name, 'DELETE')
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
"""


def permission_api_view_required(module_name, permission_name):
	def decorator(view_func):
		@wraps(view_func)
		def wrapped_view(request, *args, **kwargs):
			user = request.user
			if not user:
				# User not found, deny access
				return HttpResponseForbidden("User not found")
			
			module = Module.objects.filter(module_name=module_name).first()
			if not module:
				# Module not found, deny access
				return HttpResponseForbidden("Module not found")
			
			user_roles = user.roles.all()
			if not user_roles:
				# User has no roles, deny access
				return HttpResponseForbidden("User has no roles")
			
			# Retrieve the module permissions for the user's roles
			accesses = ModulePermission.objects.filter(
				module=module,
				permission__permission_name=permission_name,
				role__in=user_roles
			)
			
			if not accesses:
				# No permission found for any of the user's roles, deny access
				return HttpResponseForbidden("Access denied")
			
			# Permission found for at least one of the user's roles, grant access
			return view_func(request, *args, **kwargs)
		
		return wrapped_view
	
	return decorator


# +--------------------------------------------------+
# @param: Access control:
# @param: views.py
# @param: Apply on api_view
# +--------------------------------------------------+
# Example
"""
    from ..utils.UserAccessPermission import permission_api_view_required
    module_name = 'POSITION' # Replace your module name

    @api_view(['GET'])
    @permission_api_view_required(module_name, 'LIST')   
    def list(request):
        return super().list(request)
"""
