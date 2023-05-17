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
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import VerificationRequest
from artists.models import Artist


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

        if data.get("is_staff"):
            user.is_staff = data.get("is_staff")

        user.save()

        # Return JSON response with success message
        return JsonResponse(
            {"success": True, "message": "User created successfully", "id": user.id}
        )


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
        if user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=401)
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
        if user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=401)
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


@login_required
def verification_request(request, pk):
    if request.method == "POST":
        user = get_object_or_404(User, pk=pk)
        if user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        data = json.loads(request.body)
        name = data.get("name")
        if data.get("bio"):
            bio = data.get("bio")
        else:
            bio = None
        verification_request = VerificationRequest.objects.create(
            user=user, name=name, bio=bio
        )
        return JsonResponse({"message": "verification request submitted successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


@user_passes_test(lambda u: u.is_staff)
def verification_request_list(request):
    verification_requests = VerificationRequest.objects.all()
    data = []
    for request in verification_requests:
        data.append(
            {
                "id": request.id,
                "user": request.user.username,
                "name": request.name,
                "bio": request.bio,
                "approval status": request.approval_status,
            }
        )
    return JsonResponse(data, safe=False)


@user_passes_test(lambda u: u.is_staff)
def verification_request_approval(request, pk):
    if request.method == "PATCH":
        user = get_object_or_404(User, pk=pk)
        verification_request = get_object_or_404(VerificationRequest, user=user)
        data = json.loads(request.body)
        approval = data.get("approval_status")
        if approval == "approved":
            verification_request.approval_status = approval
            user.is_verified = True
            artist = Artist.objects.create(
                name=verification_request.name, user=user, bio=verification_request.bio
            )
            artist.save()
            verification_request.save()
            user.save()
            return JsonResponse(
                {
                    "message": f"{verification_request.name} has been verified.",
                    "approval status": verification_request.approval_status,
                    "is verified": user.is_verified,
                    "name": artist.name,
                }
            )
        elif approval == "rejected":
            verification_request.approval_status = approval
            verification_request.save()
            return JsonResponse(
                {
                    "message": f"{verification_request.name} has been rejected.",
                    "approval status": verification_request.approval_status,
                    "is verified": user.is_verified,
                }
            )
        else:
            return JsonResponse({"error": "Invalid approval status"})
    return JsonResponse({"error": "Invalid request method"})
