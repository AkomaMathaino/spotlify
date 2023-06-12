from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from artists.models import Artist
from albums.models import Album
from .models import Song


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

        # Set up the API client
        self.client = APIClient()
        self.client.login(username="testuser", password="testpassword")

    def test_song_list_post(self):
        # Prepare the song data
        song_data = {"title": "title1", "genre": "genre", "length": "PT3M30S"}

        # Send a POST request to the song_list endpoint
        response = self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            song_data,
            format="json",
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], song_data["title"])
        self.assertEqual(response.json()["genre"], song_data["genre"])

    def test_song_list_get(self):
        song1_data = {"title": "title1", "genre": "genre", "length": "PT3M30S"}

        song2_data = {"title": "title2", "length": "PT2M45S"}

        self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            song1_data,
            format="json",
        )
        self.client.post(
            reverse("song_list", args=[self.user.pk, self.album.pk]),
            song2_data,
            format="json",
        )
        response = self.client.get(
            reverse("song_list", args=[self.user.pk, self.album.pk]), format="json"
        )
        songs = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(songs[0]["title"], song1_data["title"])
        self.assertEqual(songs[0]["genre"], song1_data["genre"])
        self.assertEqual(songs[1]["title"], song2_data["title"])
