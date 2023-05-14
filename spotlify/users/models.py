from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None, **extra_fields):
        # extra_fields.setdefault("is_staff", False)
        # extra_fields.setdefault("is_superuser", False)
        if not username:
            raise ValueError("The Username field must be set")
        if not password:
            raise ValueError("The Password field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, email, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser):
    objects = UserManager()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=500)
    email = models.EmailField(max_length=50, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
