from django.db import models
from django.conf import settings
from songs.models import Song


# Create your models here.
class Playlist(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, blank=True, related_name="playlist_songs")
