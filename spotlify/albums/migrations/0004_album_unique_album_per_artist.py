# Generated by Django 4.2.1 on 2023-05-20 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0003_alter_album_collaborators'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='album',
            constraint=models.UniqueConstraint(fields=('title', 'primary_artist'), name='unique_album_per_artist'),
        ),
    ]
