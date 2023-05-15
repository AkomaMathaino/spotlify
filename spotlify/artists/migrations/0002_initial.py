# Generated by Django 3.2.2 on 2023-05-15 23:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('albums', '0001_initial'),
        ('artists', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistsong',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='songs.song'),
        ),
        migrations.AddField(
            model_name='artistalbum',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='albums.album'),
        ),
        migrations.AddField(
            model_name='artistalbum',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artists.artist'),
        ),
        migrations.AddField(
            model_name='artist',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
