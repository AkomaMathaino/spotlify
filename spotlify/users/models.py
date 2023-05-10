from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=False, unique=True)
    password = models.CharField(max_length=500, blank=False)
    email = models.EmailField(max_length=50, unique=True)

    USERNAME_FIELD = "username"
