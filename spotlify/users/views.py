from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import BadHeaderError
from django.template import loader
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
User = get_user_model()


def register(request):
    # Only accept POST requests
    if request.method == "POST":
        # Parse JSON data from request body
        if not request.body:
            return JsonResponse({"error": "No data provided"}, status=400)
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        # Create new user object
        user = User(username=data.get("username"), email=data.get("email"))
        user.set_password(data.get("password"))
        user.save()

        # Return JSON response with success message
        return JsonResponse({"success": True, "message": "User created successfully"})


def login_user(request):
    if request.method == "POST":
        if not request.body:
            return JsonResponse({"error": "No data provided"}, status=400)
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response_data = {"success": True, "message": "Login successful"}
            return JsonResponse(response_data)
        else:
            response_data = {"success": False, "message": "Invalid credentials"}
            return JsonResponse(response_data, status=401)


@login_required
def logout_user(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"logout": "successful"})


@login_required
def get_user_info(request, pk):
    if request.method == "GET":
        user = get_object_or_404(User, pk=pk)
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        return JsonResponse(data)


@login_required
def update_user_info(request, pk):
    if request.method == "PUT":
        user = get_object_or_404(User, pk=pk)
        data = json.loads(request.body)
        if data.get("username"):
            user.username = data.get("username")
        if data.get("password"):
            user.set_password(data.get("password"))
        if data.get("email"):
            user.email = data.get("email")
        user.save()
        return JsonResponse({"message": "User info updated successfully"})
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
