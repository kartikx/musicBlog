import requests
import base64
import datetime
import random
from urllib.parse import urlencode

"""
I'll instantiate this class in a global variable,
which persists accross multiple View requests.
This has the benefit that I won't need to make
multiple authorization calls. 
Each instance will serve for 60 minutes before
needing to be authorized again.
"""
class SpotifyClient:
    client_id = None
    client_secret = None
    access_token = None
    expires_at = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_client_creds(self):
        return f'{self.client_id}:{self.client_secret}'
    
    def get_client_creds_b64(self):
        return base64.b64encode(self.get_client_creds().encode())
    
    def get_expiration_time(self):
        return self.expires_at

    def get_access_token(self):
        if self.access_token is not None and self.expires_at is not None and \
           self.expires_at > datetime.datetime.now():
            return self.access_token
        
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_data = {
            'grant_type': 'client_credentials'
        }
        auth_header = {
            'Authorization': f"Basic {self.get_client_creds_b64().decode()}"
        }

        r = requests.post(auth_url, data= auth_data, headers= auth_header)

        if r.status_code not in range(200, 299):
            raise Exception("Something went wrong")

        self.access_token = r.json()['access_token']
        expires_in = r.json()['expires_in']
        self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds= expires_in)

        return self.access_token

    def get_track(self, song_name, artist_name, search_type= 'track'):
        access_token = self.get_access_token()
        if access_token is None:
            raise Exception("Unable to receive access token")

        endpoint = "https://api.spotify.com/v1/search"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        query_string = song_name + ' ' + artist_name
        data = urlencode({
            'q' : query_string,
            'type' : search_type
        })

        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers = headers)

        if r.status_code not in range(200, 299):
            return {}

        return r.json()
    
    def get_first_track_result(self, song_name, artist_name):
        search_result_json = self.get_track(song_name, artist_name, 'track')

        if not search_result_json:
            return {}

        first_track_result = search_result_json['tracks']['items'][0]

        return first_track_result

    def get_first_track_album_image_url(self, song_name, artist_name):
        first_track_result = self.get_first_track_result(song_name, artist_name)

        # If nothing found return a default Album Image.
        if not first_track_result:
            return 'https://i.scdn.co/image/ab67616d0000b2737a799cc62e624fd6432779e3'

        album_image_url = first_track_result['album']['images'][0]['url']
        return album_image_url

    def get_spotify_link(self, song_name, artist_name):
        first_track_result = self.get_first_track_result(song_name, artist_name)

        # If nothing found return empty url.
        if not first_track_result:
            return ''

        spotify_link = first_track_result['external_urls']['spotify']

        return spotify_link

    def get_genre_for_track(self, song_name, artist_name):
