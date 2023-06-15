from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from artists.models import Artist


# Create your tests here.
class AlbumListTestCase(TestCase):
    def setUp(self):
        # Create test users, artists, and albums
        User = get_user_model()
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.artist1 = Artist.objects.create(name="Test Artist 1", user=self.user1)

        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword", email="testemail@gmail.com"
        )
        self.artist2 = Artist.objects.create(name="Test Artist 2", user=self.user2)
        self.album1_data = {"title": "Test Album 1", "year": 2023}

        self.album2_data = {
            "title": "Test Album 2",
            "year": 2020,
            "collaborators": ["Test Artist 2"],
        }

        # Set up the API client
        self.client = APIClient()
        self.client.login(username="testuser1", password="testpassword")

    def test_album_list_post(self):
        # Test album creation
        response = self.client.post(
            reverse("album_list", args=[self.user1.pk]), self.album2_data, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], self.album2_data["title"])
        self.assertEqual(response.json()["year"], self.album2_data["year"])
        self.assertEqual(response.json()["primary_artist"], self.artist1.pk)
        self.assertEqual(response.json()["collaborators"].pop(), self.artist2.pk)

    def test_album_list_get(self):
        # Test album retrieval
        self.client.post(
            reverse("album_list", args=[self.user1.pk]), self.album1_data, format="json"
        )
        self.client.post(
            reverse("album_list", args=[self.user1.pk]), self.album2_data, format="json"
        )
        response = self.client.get(
            reverse("album_list", args=[self.user1.pk]), format="json"
        )
        albums = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(albums[0]["title"], self.album1_data["title"])
        self.assertEqual(albums[0]["year"], self.album1_data["year"])
        self.assertEqual(albums[1]["title"], self.album2_data["title"])
        self.assertEqual(albums[1]["year"], self.album2_data["year"])
        self.assertEqual(albums[1]["collaborators"].pop(), self.artist2.pk)

    def test_album_delete(self):
        # Test album deletion
        response = self.client.post(
            reverse("album_list", args=[self.user1.pk]), self.album1_data, format="json"
        )

        album_id = response.json()["id"]

        response = self.client.delete(
            reverse("album_delete", args=[self.user1.pk, album_id])
        )

        self.assertEqual(response.status_code, 200)
