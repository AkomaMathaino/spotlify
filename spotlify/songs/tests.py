from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from artists.models import Artist
from albums.models import Album


# Create your tests here.
class SongListTestCase(TestCase):
    def setUp(self):
        # Create a test user, artist, and album
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.artist = Artist.objects.create(name="Test Artist", user=self.user)
        self.album = Album.objects.create(title="title", year=2000)
        self.song1_data = {"title": "title1", "genre": "genre", "length": "PT3M30S"}

        self.song2_data = {"title": "title2", "length": "PT2M45S"}

        # Set up the API client
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_song_list_post(self):
        # Send a POST request to the song_list endpoint
        response = self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            self.song1_data,
            format="json",
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.song1_data["title"])
        self.assertEqual(response.json()["genre"], self.song1_data["genre"])

    def test_song_list_get(self):
        self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            self.song1_data,
            format="json",
        )
        self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            self.song2_data,
            format="json",
        )
        response = self.client.get(
            reverse("song_list", args=[self.user.pk, self.album.pk]), format="json"
        )
        songs = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(songs[0]["title"], self.song1_data["title"])
        self.assertEqual(songs[0]["genre"], self.song1_data["genre"])
        self.assertEqual(songs[1]["title"], self.song2_data["title"])

    def test_song_delete(self):
        response = self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            self.song1_data,
            format="json",
        )

        song_id = response.json()["id"]

        response = self.client.delete(
            reverse("song_delete", args=[self.user.pk, self.album.pk, song_id])
        )

        self.assertEqual(response.status_code, 200)
