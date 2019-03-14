from rest_framework import serializers
from spotify_connection.models import Spotify_Track


class Artist_Image_Serializer(serializers.Serializer):
    name = serializers.CharField(default='Thin Lizzy')
    url = serializers.CharField(required=False, allow_blank=True, max_length=100)

    def create(self,url_data,name_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        self.url = url_data
        self.name = name_data
        return self

class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spotify_Track
        fields = ('track_name', 'artist_name', 'album_name', 'album_image')