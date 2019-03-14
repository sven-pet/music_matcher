import base64
import json

import requests
import logging
import uuid

from django.http import JsonResponse

from spotify_connection.models import Spotify_User
from spotify_connection.models import Spotify_Track

import spotipy
import spotipy.util as util

from spotify_connection.serializers import FavoritesSerializer

spotify_id = 'e9c36faf168a4d30b49f0d846654dcc4'
spotify_secret = "7640a41f155849329d6e73b57610c26d"
spotify_redirect = 'http://musicmatcher-dev.eu-west-2.elasticbeanstalk.com/spotify/redirect/'
spotify_redirect_2 = 'https://musicmatcher-dev.eu-west-2.elasticbeanstalk.com/spotify/redirect/'
spotify_debuggertoken = "BQBt-BJXfW60QElNcJPpKFkZAd3ZrP_KYfKliJTnnfQEfI41db_G0RCbyts9g2bbhf5hjXu0HwN3_m0tZuixu_MM_wz5zQu_nI9_bDNDyP8OpKEF1fAcRbswhXBGxWoft7eYPJ4sSQVQNnmwJW4jQi8iEgeVRCxSCNr8Bqn6V0XjbTUuQHYxb1OpaR705kW8ymdM1u"

# Blog.objects.get(name="Cheddar Talk")
# Blog(name='Beatles Blog', tagline='All the latest Beatles news.') b.save()
#

logger = logging.getLogger('spotify')

def loggUser(method, user):
    logger.debug(method + " state : " + str(user.state) +
                 " user_id : " + str(user.user_id) +
                 " scope : " +  str(user.scope) +
                 " access_token : " + str(user.access_token) +
                 " refresh_token : " + str(user.refresh_token) +
                 " expires_in : " + str(user.expires_in))

def getAuthCode(user_id):
    try:
        user = Spotify_User.objects.get(user_id=user_id)
        token = user.access_token
        if token == "":
            return "error"
        return token

    except Spotify_User.DoesNotExist:
        return "error"
    #return "BQBlXeuxP-Hd7UpQuN5Nq76C5Vyln_JL0__W6bqildsbEorCp5OAJLC0f9049ZH_ekC8GeoQe0KDkznhUJtLJxnpk-pMZ6v7U97bjiM4hnnzWXlweefYMR9Rj2FNcwilM7X9O5nbFn_7SLVgOUW4X1jpkZUymeWJnWWLhYgzAyFHW2aEGVGnJjIIJwWHChRrgYwtiULOj9V2"

def getState(user_id):
    state = str(uuid.uuid4())
    try:
        user = Spotify_User.objects.get(user_id=user_id)
        user.state = state
        user.save()
        loggUser("getState after save",user)
    except Spotify_User.DoesNotExist:
        user = Spotify_User(user_id = user_id, state = state)
        user.save()
    return state

def fillDatabaseWithToken(state,resultDict):
    try:
        logger.debug("State is : " + state)
        user = Spotify_User.objects.get(state=state)
        logger.debug("Saved State is : " + user.state)
        user.scope = resultDict['scope']
        user.access_token = resultDict['access_token']
        user.refresh_token = resultDict['refresh_token']
        user.expires_in = resultDict['expires_in']
        user.save()
        loggUser("fillDatabaseWithToken after save", user)
    except Spotify_User.DoesNotExist:
        logger.debug("User does not exsist")
        return "nok"
    return "ok"

def getFavoriteTracks(user_id):
    try:
        user = Spotify_User.objects.get(user_id=user_id)
        favorits = Spotify_Track.objects.filter(users=user)
        serializer = FavoritesSerializer(favorits, many=True)
        return okResponse(serializer.data)
    except Spotify_User.DoesNotExist:
        return startAuthorization(user_id)



def setFavoriteTracks(user_id, favorits):
    for favorit in favorits:
        track_name=favorit['name']
        track_uri = favorit['uri']

        artist_list = favorit['artists']
        artist_name = artist_list[0]['name']
        artist_uri = artist_list[0]['uri']
        print ("prut")

        album = favorit['album']
        album_name = album['name']
        album_uri = album['uri']
        album_image = album['images'][0]['url']

        try:
            user = Spotify_User.objects.get(user_id=user_id)
            try:
                track = Spotify_Track.objects.get(track_id = favorit['uri'])
                track.users.add(user)
                track.save()
            except Spotify_Track.DoesNotExist:
                track = Spotify_Track(track_id=track_uri,
                                  track_name=track_name,
                                  artist_name = artist_name,
                                  artist_uri = artist_uri,
                                  album_name=album_name,
                                  album_uri=album_uri,
                                  album_image=album_image,
                                  )
                track.save()
                track.users.add(user)
                track.save()
        except Spotify_User.DoesNotExist:
            return startAuthorization(user_id)


        '''try:
            favorite = Spotify_Favorite_Track.objects.get(track_id = favorit['uri'],user_id =user_id)
        except Spotify_Favorite_Track.DoesNotExist:
            favorite = Spotify_Favorite_Track(track_id = track_uri,user_id =user_id)
            favorite.save()'''

    return ""

def logoutSpotify():
    url = 'http:// www.spotify.com/logout'
    r = requests.get(url)

def startAuthorization(user_id):
    payload = {
        'scope': 'user-top-read,'
                 'user-read-recently-played,'
                 'user-read-email,'
                 'user-read-birthdate,'
                 'user-read-private,'
                 'playlist-read-collaborative,'
                 'playlist-read-private,'
                 'user-library-read,'
                 'user-read-playback-state,'
                 'user-read-currently-playing',
        'response_type' : 'code',
        'client_id' : spotify_id,
        'redirect_uri' : spotify_redirect,
        'state' : getState(user_id),
        'show_dialog' : 'true'
    }

    url = 'http://accounts.spotify.com/authorize'
    r = requests.get(url, params=payload)
    return r.url

def requestAccessToken(request):
    code = request.GET.get('code', default=None)
    data = {
        'grant_type': 'authorization_code',
        'code' : code,
        'redirect_uri' : spotify_redirect,
        'client_id': spotify_id,
        'client_secret': spotify_secret
    }

    '''
    'client_id' :spotify_id,
    'client_secret' : spotify_secret,
    '''
    encodeString = spotify_id + ':' + spotify_secret
    #headers = {'Authorization': 'Basic ' + base64.b64encode(encodeString)}
    url = 'https://accounts.spotify.com/api/token'

    r = requests.post(url, data=data)
    dictdump = r.json()
    state = request.GET.get('state', default=None)
    fillDatabaseWithToken(state,dictdump)
    result = {
        "content": dictdump['access_token'],
        "refresh": dictdump['refresh_token']
    }

    return okResponse(result,"1")

def requestFavoritArtists(request,user_id):
    authcode = getAuthCode(user_id)

    if(authcode != 'error'):
        headers = {'Authorization': 'Bearer ' + getAuthCode(user_id)}

        payload = {}
        url = 'https://api.spotify.com/v1/me/top/artists'
        r = requests.get(url, headers=headers)
        result = {
            "code": r.status_code,
            "reason":r.reason,
            "content":r.json()
        }
        return result
    else:
        result = {
              "error": "Can´t fetch token"
        }
        return result

def requestFavoritTracks(request,user_id):
    try:
        user = Spotify_User.objects.get(user_id=user_id)
    except Spotify_User.DoesNotExist:
        return needToReconnect()

    #user_id = request.GET.get('user_id', default='sven')
    authcode = getAuthCode(user_id)

    if(authcode != 'error'):
        headers = {'Authorization': 'Bearer ' + getAuthCode(user_id)}

        payload = {}
        url = 'https://api.spotify.com/v1/me/top/tracks'
        r = requests.get(url, headers=headers)
        json = r.json()
        result = {
            "code": r.status_code,
            "reason":r.reason,
            "content":r.json()
        }

        if(r.status_code == 401):
            return refreshAccessToken(user_id)

        jitem = json["items"]
        setFavoriteTracks(user_id,jitem)
        r = getFavoriteTracks(user_id)
        #return r
        return r
    else:
        '''result = {
              "error": "Can´t fetch token"
        }
        return result'''
        return needToReconnect()

def refreshAccessToken(user_id):
    try:
        user = Spotify_User.objects.get(user_id=user_id)
        loggUser("refreshing ", user)
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': user.refresh_token,
            'client_id': spotify_id,
            'client_secret': spotify_secret
        }
        url = 'https://accounts.spotify.com/api/token'

        r = requests.post(url, data=data)
        dictdump = r.json()
        if 'access_token' in dictdump.keys():
            accessToken = dictdump['access_token']
            user.access_token = accessToken
            user.save()
            return dictdump
        return needToReconnect()
    except Spotify_User.DoesNotExist:
        return needToReconnect()
    return

def requestAlbum(request):
    user_id = request.GET.get('user_id', default='sven')
    spotify_id = request.GET.get('spotify_id', default='')
    authcode = getAuthCode(user_id)

    if(authcode != 'error'):
        headers = {'Authorization': 'Bearer ' + getAuthCode(user_id)}

        '''payload = {
            'ids': 
        }'''
        url = 'https://api.spotify.com/v1/me/top/tracks'
        r = requests.get(url, headers=headers)
        result = {
            "code": r.status_code,
            "reason":r.reason,
            "content":r.json()
        }
        return result
    else:
        result = {
              "error": "Can´t fetch token"
        }
        return result


def needToReconnect():
    result = {
        "status": "2",
        "reason": " You need to reconnect",
        "payload" : ""
    }
    return result

def okResponse(result, status = "0"):
    result = {
        "status": status,
        "reason": "ok",
        "payload": result
    }
    return result





