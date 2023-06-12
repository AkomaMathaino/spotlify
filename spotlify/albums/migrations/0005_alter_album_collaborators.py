# Generated by Django 4.2.1 on 2023-06-12 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artists', '0003_remove_artistsong_artist_remove_artistsong_song_and_more'),
        ('albums', '0004_album_unique_album_per_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='collaborators',
            field=models.ManyToManyField(blank=True, related_name='collaborator_albums', to='artists.artist'),
        ),
    ]
