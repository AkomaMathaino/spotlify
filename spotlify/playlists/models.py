from django.db import models
from django.conf import settings


# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
