from django.db import models
from albums.models import Album


# Create your models here.
class Song(models.Model):
    title = models.CharField(max_length=20)
    genre = models.CharField(max_length=20, blank=True, null=True)
    streams = models.PositiveIntegerField(default=0)
    length = models.DurationField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
