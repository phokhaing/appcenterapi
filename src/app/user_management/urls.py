# from rest_framework.routers import DefaultRouter
# from .views import UserManagement
#
# router = DefaultRouter()
# router.register('', viewset=UserManagement, basename='users')  # ModelViewSet
# # router.register('/logout', viewset=UserLogout, basename='logout')  # ModelViewSet
#
# urlpatterns = router.urls
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserManagement,
    ChangePasswordView,
    UpdateProfileView,
    SuspendedUserView,
    ResetPasswordView,
    ModuleListCreateAPIView,
    ModuleRetrieveAPIView,
    ModuleUpdateAPIView,
    ModuleDestroyAPIView,
    ModuleListingApiView,
    ListPermissionByModuleIDAPIView,
    SavePermissionToModuleAPIView,
    ListPermissionNotExistingByModuleIDAPIView,
    DeletePermissionToModuleAPIView,
    PermissionListCreateAPIView,
    PermissionRetrieveAPIView,
    PermissionUpdateAPIView,
    PermissionDestroyAPIView,
    PermissionListingApiView,
    RoleListCreateAPIView,
    RoleRetrieveAPIView,
    RoleUpdateAPIView,
    RoleDestroyAPIView,
    RoleListingApiView,
    ListModuleByRoleIDAPIView,
    SaveModuleToRoleAPIView,
    ListModuleNotExistingByRoleIDAPIView,
    DeleteModuleToRoleAPIView,
    UserPermissionsAPIView,
    ListRoleByUserIDAPIView,
    ListRoleNotExistingByUserIDAPIView,
    UpdateUserRoleAPIView,
    UserListing,
    UserListingPagination,
    UserPermissionsApprovalLog,
    GroupUserController,
)

from .views.user import set_new_password, ForgotPasswordView

# Create a router object
router = DefaultRouter()
router.register("", viewset=UserManagement, basename="manage_user")

urlpatterns = [
    path(
        "user_change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="user_change_password",
    ),
    path(
        "user_update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="user_update_profile",
    ),
    path("suspended/<int:pk>/", SuspendedUserView.as_view(), name="suspended_user"),
    path(
        "reset_password/<int:pk>/", ResetPasswordView.as_view(), name="reset_password"
    ),
    #  forgot password
    path("forgot_password/", ForgotPasswordView.as_view(), name="forgot_password"),
    # set new password
    path("set_new_password/", set_new_password, name="set_new_password"),
    # module
    path("module/", ModuleListCreateAPIView.as_view(), name="module-list"),
    path("module/<int:pk>/", ModuleRetrieveAPIView.as_view(), name="module-retrieve"),
    path(
        "module/<int:pk>/update/", ModuleUpdateAPIView.as_view(), name="module-update"
    ),
    path(
        "module/<int:pk>/delete/", ModuleDestroyAPIView.as_view(), name="module-delete"
    ),
    path("module_listing/", ModuleListingApiView.as_view(), name="module_listing"),
    path(
        "module/list_permission/by/role/<int:role_id>/module/<int:module_id>/",
        ListPermissionByModuleIDAPIView.as_view(),
        name="list_permission_by_module",
    ),
    path(
        "module/list_permission_not_existing/by/role/<int:role_id>/module/<int:module_id>/",
        ListPermissionNotExistingByModuleIDAPIView.as_view(),
        name="list_permission_not_existing_by_module",
    ),
    path(
        "module/save_permission/",
        SavePermissionToModuleAPIView.as_view(),
        name="save_permission",
    ),
    path(
        "module/delete_permission/<int:pk>/",
        DeletePermissionToModuleAPIView.as_view(),
        name="delete_permission",
    ),
    # permission
    path("permission/", PermissionListCreateAPIView.as_view(),
         name="permission-list"),
    path(
        "permission/<int:pk>/",
        PermissionRetrieveAPIView.as_view(),
        name="permission-retrieve",
    ),
    path(
        "permission/<int:pk>/update/",
        PermissionUpdateAPIView.as_view(),
        name="permission-update",
    ),
    path(
        "permission/<int:pk>/delete/",
        PermissionDestroyAPIView.as_view(),
        name="permission-delete",
    ),
    path(
        "permission_listing/",
        PermissionListingApiView.as_view(),
        name="permission_listing",
    ),
    path(
        "permission/access/", UserPermissionsAPIView.as_view(), name="permission_access"
    ),
    # role
    path("role/", RoleListCreateAPIView.as_view(), name="role-list"),
    path("role/<int:pk>/", RoleRetrieveAPIView.as_view(), name="role-retrieve"),
    path("role/<int:pk>/update/", RoleUpdateAPIView.as_view(), name="role-update"),
    path("role/<int:pk>/delete/", RoleDestroyAPIView.as_view(), name="role-delete"),
    path("role_listing/", RoleListingApiView.as_view(), name="role_listing"),
    path(
        "role/list_module/by/role/<int:role_id>/",
        ListModuleByRoleIDAPIView.as_view(),
        name="list_module_by_role",
    ),
    path(
        "role/list_module_not_existing/by/role/<int:role_id>/",
        ListModuleNotExistingByRoleIDAPIView.as_view(),
        name="list_module_not_existing_by_role",
    ),
    path("role/save_module/", SaveModuleToRoleAPIView.as_view(), name="save_module"),
    path(
        "role/delete_module/row_id/<int:row_id>/module_id/<int:module_id>/role_id/<int:role_id>",
        DeleteModuleToRoleAPIView.as_view(),
        name="delete_module",
    ),
    path(
        "list_role/by/user/<int:user_id>/",
        ListRoleByUserIDAPIView.as_view(),
        name="list_role_by_user",
    ),
    path(
        "list_role_not_existing/by/user/<int:user_id>/",
        ListRoleNotExistingByUserIDAPIView.as_view(),
        name="list_role_not_existing_by_user",
    ),
    path(
        "user_role/<int:user_id>/update-role/",
        UpdateUserRoleAPIView.as_view(),
        name="update_user_role",
    ),
    path("user-listing/", UserListing.as_view(), name="user-listing"),
    path(
        "user_listing_pagination/",
        UserListingPagination.as_view(),
        name="user_listing_pagination",
    ),
    path(
        "permission/access/approval_log/",
        UserPermissionsApprovalLog.as_view(),
        name="user_permission_approval_log",
    ),
    # ******************************** #
    # ********** GRUOP USER ********** #
    # ******************************** #
    path("group_user_existing/<int:group_id>/",
         GroupUserController.existing_user_listing,
         name="group_user_existing"
         ),
    path("group_listing/",
         GroupUserController.list_group_user,
         name="group_listing"
         ),
    path(
        "group_user_create/",
        GroupUserController.create_group_user,
        name="group_user_create",
    ),
    path(
        "group_user_update/<int:id>/",
        GroupUserController.update_group_user,
        name="group_user_update",
    ),
    path(
        "group_user_view/<int:id>/",
        GroupUserController.view_group_user,
        name="group_user_view",
    ),
    path(
        "group_user_delete/<int:id>/",
        GroupUserController.delete_group_user,
        name="group_user_delete",
    ),
    path(
        "group_listing_membership/<int:group_id>/",
        GroupUserController.list_membership,
        name="group_listing_membership",
    ),
    path(
        "group_add_membership/",
        GroupUserController.create_group_membership,
        name="add_group_membership",
    ),
    # path(
    #     "get_users_in_group/<int:group_id>/",
    #     GroupUserController.get_users_in_group,
    #     name="get_users_in_group",
    # ),
    path(
        "group_delete_membership/<int:id>/",
        GroupUserController.delete_user_membership,
        name="group_delete_membership",
    ),
] + router.urls
