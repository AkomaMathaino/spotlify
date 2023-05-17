from django.test import TestCase
import pytest
from rest_framework.test import APIClient
import json
from .models import User
from django.test import RequestFactory
from django.urls import reverse


# Create your tests here.
client = APIClient()


@pytest.fixture
def register_user():
    url = "/api/register/"
    payload = dict(username="john", password="password", email="john@gmail.com")
    return client.post(url, payload, format="json").json()


@pytest.mark.django_db
def test_register_user(register_user):
    assert register_user["success"]


@pytest.fixture
def login_user(register_user):
    url = "/api/login/"
    payload = dict(username="john", password="password")
    return client.post(url, payload, format="json").json()


@pytest.mark.django_db
def test_login_user(login_user):
    assert login_user["success"]


@pytest.mark.django_db
def test_verification_request(register_user, login_user):
    url = f"/api/verification_request/{register_user['id']}"
    payload = dict(name="john doe")
    client.force_authenticate(user=User.objects.get(id=register_user["id"]))
    response = client.post(url, payload, format="json", follow=True)
    print(response.content)
    assert response.status_code == 200
