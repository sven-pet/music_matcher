from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('<userid>/connect/', views.Spotify_getToken, name="token"),
    path('redirect/', views.Spotify_redirect, name="redirect"),
    path('swagger/', schema_view),
    path('<userid>/favorite_artist/',views.Spotify_getFavoritArtist, name="favoritArtist"),
    path('<userid>/favorite_track/',views.Spotify_getFavoritTrack, name="favoritTrack"),
    path('<userid>/', views.Spotify_getUser, name="user")
   #path('<userid>/reconnect/', views.Spotify_getToken, name="token")
]