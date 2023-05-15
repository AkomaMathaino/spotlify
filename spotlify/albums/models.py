from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


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
