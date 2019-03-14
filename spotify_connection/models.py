from django.db import models

# Create your models here.

class Spotify_User(models.Model):
    user_id = models.CharField(max_length=200,default='')
    state = models.CharField(max_length=200,default='')
    access_token = models.CharField(max_length=200,default='')
    scope = models.CharField(max_length=200,default='')
    expires_in = models.IntegerField(default=0)
    refresh_token = models.CharField(max_length=200,default='')

class Spotify_Track(models.Model):
    track_id = models.CharField(max_length=30,default='')
    track_name = models.CharField(max_length=30,default='')
    artist_name = models.CharField(max_length=30,default='')
    artist_uri = models.CharField(max_length=30,default='')
    album_name = models.CharField(max_length=30,default='')
    album_uri = models.CharField(max_length=30,default='')
    album_image = models.CharField(max_length=60,default='')
    users = models.ManyToManyField(Spotify_User)

