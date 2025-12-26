from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("employee/add/", views.add_employee, name="add_employee"),
    path("employee/save/", views.save_employee, name="save_employee"),
    path("employee/get-users/", views.get_users, name="get_users"),
    path("employee/get/<int:id>/", views.edit_user, name="edit_user"),
    path("employee/update-employee/", views.update_employee, name="update_employee"),
    path("employee/delete/<int:id>/", views.delete, name="delete"),
]
