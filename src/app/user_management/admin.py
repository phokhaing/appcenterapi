from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    User,
    UserRole,
    Role,
    RoleModule,
    Module,
    ModulePermission,
    Permission,
    UserAvatar,
    GroupsUser,
    GroupMembership
)


class UserRoleInline(admin.TabularInline):
    model = User.roles.through
    extra = 1


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 0


# class RoleModuleInline(admin.TabularInline):
#     model = Role.modules.through
#     extra = 1


# class ModulePermissionInline(admin.TabularInline):
#     model = Module.permissions.through
#     extra = 1


class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [UserRoleInline]
    list_display = [
        "staff_id",
        "username",
        "fullname",
        "email",
        "get_role_name",
        "get_position",
        "get_department",
        "get_branch",
        "is_active",
    ]

    def get_role_name(self, obj):
        return ", ".join(role.role_name_en for role in obj.roles.all())

    def get_position(self, obj):
        return obj.position.name_en if obj.position else None

    def get_department(self, obj):
        return obj.department.name_en if obj.department else None

    def get_branch(self, obj):
        return obj.branch.name_en if obj.branch else None

    get_role_name.short_description = "Role Name"
    get_position.short_description = "Position"
    get_department.short_description = "Department"
    get_branch.short_description = "Branch"

    list_display_links = ["staff_id", "username"]
    search_fields = [
        "staff_id",
        "first_name",
        "last_name",
        "first_name_kh",
        "last_name_kh",
        "username",
        "email",
    ]


class RoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["role_name_en"]


class ModuleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["module_name"]


class UserRoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "role"]


class RoleModuleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "role", "module"]


class ModulePermissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "role", "module"]


class PermissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "permission_name"]


class UserAvatarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ["id", "user_id", "upload_file_name", "file_path"]


# class RoleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     inlines = [RoleModuleInline]


# class ModuleAdmin(admin.ModelAdmin):
#     inlines = [ModulePermissionInline]


class GroupsUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'hook',
        'status',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at'
    )

    list_display_links = ['id', 'title', 'hook',]

    inlines = [GroupMembershipInline]


class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'group_id',
        'user_id',
        'status',
        'created_by',
        'created_at',
        'updated_by',
        'updated_at'
    )

    list_display_links = ['id', 'group_id', 'user_id',]


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(RoleModule, RoleModuleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(ModulePermission, ModulePermissionAdmin)
admin.site.register(UserAvatar, UserAvatarAdmin)
admin.site.register(GroupsUser, GroupsUserAdmin)
admin.site.register(GroupMembership, GroupMembershipAdmin)

# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#    list_display = [
#       "staff_id",
#       "fullname",
#       "gender",
#       "email",
#       "pc_id",
#       "ip_address",
#       "is_active",
#    ]
#    list_display_links = ["staff_id", "fullname"]
