from django.urls import path
from . import views

urlpatterns = [
    path("static/", views.index_emp, name="index"),
    path("add/", views.add_employee, name="add_employee"),
    path("save/", views.save_employee, name="save_employee"),
    path("get-users/", views.get_users, name="get_users"),
    path("get/<int:id>/", views.edit_user, name="edit_user"),
    path("update-", views.update_employee, name="update_employee"),
    path("delete/<int:id>/", views.delete, name="delete"),
]
