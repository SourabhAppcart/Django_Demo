from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("addUser/", views.addUser, name="addUser"),
    path("save-user/", views.saveUsers, name="saveUsers"),
    path("login/", views.loginUser, name="loginUser"),
    path("logout/", views.logoutUser, name="logoutUser"),
]
