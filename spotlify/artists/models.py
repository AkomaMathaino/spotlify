from django.db import models
from django.conf import settings


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=20, unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
