from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addUser/", views.addUser, name="addUser"),
    path("save-user/", views.saveUsers, name="saveUsers"),
    path("login/", views.loginUser, name="loginUser"),
    path("logout/", views.logoutUser, name="logoutUser"),
    path("create-roles/", views.createRoles, name="createRoles"),
    path("save-roles/", views.saveRoles, name="saveRoles"),
    path("get-roles/", views.getRoles, name="getRoles"),
    path("get-roles-table/", views.getRolesTable, name="getRolesTable"),
    path("get-users/", views.getUsers, name="getUsersRoles"),
    path("edit-users/<int:id>/", views.editUser, name="editUser"),
    path("update-users/<int:id>/", views.updateUser, name="updateUser"),
    path("roles/details/<int:id>/", views.get_role_details, name="getRoleDetails"),
    path("update-role/", views.update_role, name="updateRole"),
]
