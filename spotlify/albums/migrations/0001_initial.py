# Generated by Django 3.2.2 on 2023-05-15 23:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2023, message='Year must be valid.'), django.core.validators.MinValueValidator(1900, message='Year must be after 1900.')])),
            ],
        ),
    ]