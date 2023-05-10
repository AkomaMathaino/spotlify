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

# Create your views here.
User = get_user_model()


def register(request):
    # Only accept POST requests
    if request.method == "POST":
        # Parse JSON data from request body
        try:
            data = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"})

        # Create new user object
        user = User(username=data.get("username"), email=data.get("email"))
        user.set_password(data.get("password"))
        user.save()

        # Return JSON response with success message
        return JsonResponse({"success": True, "message": "User created successfully"})
