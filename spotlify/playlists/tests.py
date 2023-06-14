from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from artists.models import Artist
from albums.models import Album
from songs.models import Song
from .models import Playlist
import datetime


# Create your tests here.
class PlaylistTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.artist = Artist.objects.create(name="Test Artist", user=self.user)
        self.album = Album.objects.create(
            title="Album Title", year=2023, primary_artist=self.artist
        )
        self.song = Song.objects.create(
            title="Song Title",
            length=datetime.timedelta(minutes=3, seconds=30),
            album=self.album,
        )
        self.playlist_data = {"title": "Playlist Title"}

        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_playlist_list_post(self):
        response = self.client.post(
            reverse("playlist_list", args=[self.user.pk]),
            self.playlist_data,
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.playlist_data["title"])
        self.assertEqual(response.json()["user"], self.user.pk)

    def test_playlist_get(self):
        playlist = Playlist.objects.create(title="Playlist Title", user=self.user)

        response1 = self.client.get(
            reverse("playlist_list", args=[self.user.pk]), format="json"
        )
        playlists = response1.json()

        response2 = self.client.get(
            reverse("playlist_specific", args=[self.user.pk, playlist.pk]),
            format="json",
        )
        playlist_data = response2.json()

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(playlists[0]["title"], playlist.title)
        self.assertEqual(playlists[0]["user"], self.user.pk)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(playlist_data["title"], playlist.title)
        self.assertEqual(playlist_data["user"], self.user.pk)

    def test_playlsit_delete(self):
        response = self.client.post(
            reverse("playlist_list", args=[self.user.pk]),
            self.playlist_data,
            format="json",
        )

        playlist_id = response.json()["id"]

        response = self.client.delete(
            reverse("playlist_specific", args=[self.user.pk, playlist_id])
        )

        self.assertEqual(response.status_code, 200)

    def test_playlist_patch(self):
        response = self.client.post(
            reverse("playlist_list", args=[self.user.pk]),
            self.playlist_data,
            format="json",
        )

        playlist_id = response.json()["id"]

        songs = [self.song.pk]
        print(songs)
        r = self.client.patch(
            reverse("playlist_specific", args=[self.user.pk, playlist_id]),
            {"songs": songs},
            format="json",
        )

        response = self.client.get(
            reverse("playlist_specific", args=[self.user.pk, playlist_id]),
            format="json",
        )
        playlist_data = response.json()

        self.assertEqual(r.status_code, 200)
        self.assertEqual(playlist_data["songs"], songs)

        d = self.client.patch(
            reverse(
                "playlist_song_delete", args=[self.user.pk, playlist_id, self.song.pk]
            )
        )
        response = self.client.get(
            reverse("playlist_specific", args=[self.user.pk, playlist_id]),
            format="json",
        )
        playlist_data = response.json()
        songs.remove(self.song.pk)

        self.assertEqual(d.status_code, 200)
        self.assertEqual(playlist_data["songs"], songs)
