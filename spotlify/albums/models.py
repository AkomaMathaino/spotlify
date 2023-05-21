from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
from artists.models import Artist


# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=20)
    year = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(
                datetime.datetime.now().year, message="Year must be valid."
            ),
            MinValueValidator(1900, message="Year must be after 1900."),
        ]
    )
    primary_artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name="primary_album", null=True
    )
    collaborators = models.ManyToManyField(
        Artist, blank=True, related_name="collaborator_albums"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_album_per_artist", fields=["title", "primary_artist"]
            )
        ]
