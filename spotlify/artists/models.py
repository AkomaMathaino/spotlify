from django.db import models
from albums.models import Album
from songs.models import Song
from django.conf import settings


# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=20, unique=True)
    bio = models.TextField(max_length=300, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ArtistSong(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)


class ArtistAlbum(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
