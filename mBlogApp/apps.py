import os
from django.apps import AppConfig
from .spotifyclient import SpotifyClient

"""
1. What is ready(self)?
2. Is this best practice?
"""
class MblogappConfig(AppConfig):
    name = 'mBlogApp'
    # Also set up in Heroku.
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

    client = SpotifyClient(client_id = client_id, client_secret= client_secret)

    def ready(self):
        import mBlogApp.signals
