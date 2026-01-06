from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


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
        return JsonResponse({"message": "User added successfully!"})

    return JsonResponse({"message": "Invalid request method."}, status=405)
