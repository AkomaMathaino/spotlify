from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from artists.models import Artist
from .models import Album


# Create your tests here.
class AlbumListTestCase(TestCase):
    def setUp(self):
        # Create a test user and artist
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.artist1 = Artist.objects.create(name="Test Artist 1", user=self.user1)

        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword", email="testemail@gmail.com"
        )
        self.artist2 = Artist.objects.create(name="Test Artist 2", user=self.user2)

        # Set up the API client
        self.client = APIClient()
        self.client.login(username="testuser1", password="testpassword")

    def test_album_list_post(self):
        # Prepare the album data
        album_data = {
            "title": "Test Album",
            "year": 2023,
            "collaborators": ["Test Artist 2"],
        }

        # Send a POST request to the album_list endpoint
        response = self.client.post(
            reverse("album_list", args=[self.user1.pk]), album_data, format="json"
        )

        # Assert the response status code and content
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], album_data["title"])
        self.assertEqual(response.json()["year"], album_data["year"])
        self.assertEqual(response.json()["primary_artist"], self.artist1.pk)
        self.assertEqual(response.json()["collaborators"].pop(), self.artist2.pk)

    def test_album_list_get(self):
        album1_data = {"title": "Test Album 1", "year": 2023}

        album2_data = {
            "title": "Test Album 2",
            "year": 2020,
            "collaborators": ["Test Artist 2"],
        }

        self.client.post(
            reverse("album_list", args=[self.user1.pk]), album1_data, format="json"
        )
        self.client.post(
            reverse("album_list", args=[self.user1.pk]), album2_data, format="json"
        )
        response = self.client.get(
            reverse("album_list", args=[self.user1.pk]), format="json"
        )
        albums = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(albums[0]["title"], album1_data["title"])
        self.assertEqual(albums[0]["year"], album1_data["year"])
        self.assertEqual(albums[1]["title"], album2_data["title"])
        self.assertEqual(albums[1]["year"], album2_data["year"])
        self.assertEqual(albums[1]["collaborators"].pop(), self.artist2.pk)
