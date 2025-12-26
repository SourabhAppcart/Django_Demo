# employee/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import Users
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json


def index(request):
    return render(request, "emp_static.html")


def add_employee(request):
    return render(request, "emp_add.html")


def save_employee(request):
    if request.method == "POST":
        print("Request POST Data:", request.POST)  # Debug print

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check duplicate email
        if Users.objects.filter(email=email).exists():
            return JsonResponse(
                {"message": "User with this email already exists."}, status=400
            )

        # Hash password
        hashed_password = make_password(password)

        Users.objects.create(name=name, email=email, password=hashed_password)

        return JsonResponse({"message": "Employee added successfully."})

    # For other methods, return Method Not Allowed response
    return HttpResponse("Only POST requests are allowed.", status=405)


def get_users(request):
    users = Users.objects.order_by("-id").values()

    users_list = list(users)
    for u in users_list:
        if u.get("create_at"):
            u["create_at"] = u["create_at"].strftime("%Y-%m-%d %H:%M")

    return JsonResponse({"data": users_list})


def edit_user(request, id):
    user = Users.objects.get(id=id)
    return JsonResponse(
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        }
    )


def update_employee(request):
    if request.method == "POST":
        user_id = request.POST.get("id")
        new_email = request.POST.get("email")
        new_name = request.POST.get("name")

        # Check if the email is used by another user (excluding current user)
        if Users.objects.filter(email=new_email).exclude(id=user_id).exists():
            return JsonResponse(
                {"status": "error", "message": "Email already exists"}, status=400
            )

        try:
            user = Users.objects.get(id=user_id)
            user.name = new_name
            user.email = new_email
            user.save()
            return JsonResponse({"status": "success"})
        except Users.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "User not found"}, status=404
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Invalid method"}, status=405
        )


def delete(request, id):
    if request.method == "DELETE":
        try:
            user = Users.objects.get(id=id)
            user.delete()
            return JsonResponse({"status": "success"})
        except Users.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "User not found"}, status=404
            )
    return JsonResponse({"status": "error", "message": "Invalid method"}, status=400)
