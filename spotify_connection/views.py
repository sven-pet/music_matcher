from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets

from django.http import HttpResponse, JsonResponse
import logging
import MusicMatcher


from spotify_connection.serializers import Artist_Image_Serializer
from spotify_connection.spotify_calls import *
from spotify_connection.models import Spotify_User
from django.db.models.query import QuerySet

logger = logging.getLogger('spotify')

def Spotify_getFavoritTrack(request,userid):
    result = requestFavoritTracks(request,userid)
    #result = {"body":result}
    '''if isinstance(result, QuerySet):
        serializer = FavoritesSerializer(result, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(result, json_dumps_params={'indent': 2})'''
    return JsonResponse(result, json_dumps_params={'indent': 2})

def Spotify_getFavoritArtist(request,userid):
    result = requestFavoritArtists(request,userid)
    #result = {"body":result}
    return JsonResponse(result, json_dumps_params={'indent': 2})



def Spotify_getToken(request,userid):
    """
    API endpoint that allows users to be viewed or edited.
    """
    logger.debug("Spotify_getToken : request : " + str(request.GET.dict()))
    url = startAuthorization(userid)
    newdict = {"spotify_url": url}
    logger.debug("Spotify_getToken : response : " + str(newdict))
    return JsonResponse(newdict)

def Spotify_redirect(request):
    """
    API endpoint that allows users to be viewed or edited.
    """

    logger.debug("Spotify_redirect : request : " + str(request.GET.dict()))
    if request.method == 'GET':

        if request.GET.keys().__contains__('code'):
            result = requestAccessToken(request)

        else:
            result = {"error": request.GET.get('Error', default=None),
                   "body": str(request.GET.dict())}

        logger.debug("Spotify_redirect : response : " + str(result))
        return JsonResponse(result, safe=False)
        #return HttpResponse(result)

def Spotify_getUser(request,userid):
    try:
        user = Spotify_User.objects.get(user_id=userid)
        result = {"result": "ok",
                  "status": "0",
                  "message": "User exists"}
        return JsonResponse(result, safe=False)

    except (Spotify_User.DoesNotExist):
        result = {"result": "nok",
                  "status": "1",
                  "message": "User does not exist"}
        return JsonResponse(result, safe=False)