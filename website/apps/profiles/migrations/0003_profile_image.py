# Generated by Django 3.2.9 on 2021-12-07 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_remove_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.FileField(blank=True, max_length=255, upload_to='uploads/%Y/%m/%d/'),
        ),
    ]