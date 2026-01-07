from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group, Permission
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

# import  core\roles\rolesLogic.py


# Create your views here.


def index(request):
    return render(request, "login.html")


def loginUser(request):
    if request.method == "POST":
        print(dict(request.POST))  # ✅ debug is fine

        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(
                Q(username__iexact=username_or_email)
                | Q(email__iexact=username_or_email)
            )
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect("/employee/static/")  # ✅ MUST return
        else:
            return render(
                request, "login.html", {"error": "Invalid username/email or password"}
            )  # ✅ MUST return

    # 👇 IMPORTANT: handle non-POST requests
    return redirect("/")


def logoutUser(request):
    logout(request)
    return redirect("/")


@login_required(login_url="/")
def addUser(request):
    return render(request, "pages/addUser.html")


# add detils in default table auth_user


def saveUsers(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        group_name = request.POST.get("group")

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {"message": "User with this username already exists."}, status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "User with this email already exists."}, status=400
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
        )
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user = User.objects.get(username=username)
                user.groups.add(group)
            except Group.DoesNotExist:
                return JsonResponse(
                    {"message": "Specified group does not exist."}, status=400
                )
        return JsonResponse({"message": "User added successfully!"})

    return JsonResponse({"message": "Invalid request method."}, status=405)


# create roles page
@login_required(login_url="/")
def createRoles(request):
    permissions = Permission.objects.all().order_by("content_type__model")
    return render(request, "pages/create_roles.html", {"permissions": permissions})


# save roles to database (to be implemented)
# def saveRoles(request):
#     if request.method == "POST":
#         name = request.POST.get("role_name")

#         if not name:
#             return JsonResponse(
#                 {"status": "error", "message": "Role name cannot be empty"}, status=400
#             )

#         group, created = Group.objects.get_or_create(name=name)

#         if created:
#             return JsonResponse(
#                 {"status": "success", "message": "Role created successfully"}
#             )

#         return JsonResponse(
#             {"status": "warning", "message": "Role already exists"}, status=400
#         )


def saveRoles(request):
    if request.method == "POST":
        name = request.POST.get("role_name")
        permission_ids = request.POST.getlist("permissions[]")

        # Validation
        if not name:
            return JsonResponse(
                {"status": "error", "message": "Role name cannot be empty"}, status=400
            )

        # Create role (Group)
        group, created = Group.objects.get_or_create(name=name)

        if not created:
            return JsonResponse(
                {"status": "warning", "message": "Role already exists"}, status=400
            )

        # Assign permissions (if any selected)
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)

        return JsonResponse(
            {
                "status": "success",
                "message": "Role created and permissions assigned successfully",
            }
        )

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=405)


# get all roles in json


def getRoles(request):
    roles = Group.objects.all().values_list("name",)
    # pass only name

    return JsonResponse(list(roles), safe=False)


def getRolesTable(request):
    roles = Group.objects.all().values_list("name", "id")
    # pass only name

    return JsonResponse(list(roles), safe=False)


# get user and its group


def getUsers(request):
    user = User.objects.all()
    data = []
    for u in user:
        groups = u.groups.all().values_list("name", flat=True)
        data.append(
            {
                "id": u.id,
                "username": u.username,
                "first_name": u.first_name,
                "email": u.email,
                "groups": ", ".join(groups),
            }
        )
    return JsonResponse({"data": data})


# edit user (to be implemented)


def editUser(request, id):
    try:
        user = User.objects.get(id=id)
        groups = user.groups.all().values_list("name", flat=True)
        data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "email": user.email,
            "groups": list(groups),
        }
        return JsonResponse({"status": "success", "data": data})
    except User.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "User not found"}, status=404
        )


# update user (to be implemented)
@csrf_exempt
def updateUser(request, id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=id)
            first_name = request.POST.get("first_name")
            email = request.POST.get("email")
            username = request.POST.get("username")
            group_name = request.POST.get("group")

            if User.objects.filter(username=username).exclude(id=id).exists():
                return JsonResponse(
                    {"message": "User with this username already exists."}, status=400
                )

            if User.objects.filter(email=email).exclude(id=id).exists():
                return JsonResponse(
                    {"message": "User with this email already exists."}, status=400
                )

            user.first_name = first_name
            user.email = email
            user.username = username
            user.save()

            if group_name:
                try:
                    group = Group.objects.get(name=group_name)
                    user.groups.clear()
                    user.groups.add(group)
                except Group.DoesNotExist:
                    return JsonResponse(
                        {"message": "Specified group does not exist."}, status=400
                    )

            return JsonResponse({"message": "User updated successfully!"})
        except User.DoesNotExist:
            return JsonResponse({"message": "User not found."}, status=404)

    return JsonResponse({"message": "Invalid request method."}, status=405)


# Django View to Fetch Role + Permissions
def get_role_details(request, id):
    role = Group.objects.get(id=id)
    role_permissions = role.permissions.values_list("id", flat=True)

    all_permissions = Permission.objects.all().values("id", "name")

    return JsonResponse(
        {
            "id": role.id,
            "name": role.name,
            "assigned_permissions": list(role_permissions),
            "all_permissions": list(all_permissions),
        }
    )


@csrf_exempt
def update_role(request):
    if request.method == "POST":
        role = Group.objects.get(id=request.POST.get("role_id"))
        role.name = request.POST.get("role_name")
        role.save()

        role.permissions.clear()
        role.permissions.add(*request.POST.getlist("permissions[]"))

        return JsonResponse({"message": "Role updated successfully"})
