# Generated by Django 2.1.3 on 2019-03-04 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_connection', '0004_auto_20190301_1612'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Spotify_Favorite_Track',
        ),
        migrations.AddField(
            model_name='spotify_track',
            name='users',
            field=models.ManyToManyField(to='spotify_connection.Spotify_User'),
        ),
    ]
