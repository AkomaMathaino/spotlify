# Generated by Django 4.2.1 on 2023-06-13 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='song',
            constraint=models.UniqueConstraint(fields=('title', 'album'), name='unique_song_per_album'),
        ),
    ]