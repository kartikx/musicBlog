from django.apps import AppConfig
from .spotifyclient import SpotifyClient

"""
1. What is ready(self)?
2. Is this best practice?
"""
class MblogappConfig(AppConfig):
    name = 'mBlogApp'
    client_id = "11c45ddf7bc044b6b6ebff5cf3fc77cd"
    client_secret = "ab374863a10240ab835146fc21d71205"

    client = SpotifyClient(client_id = client_id, client_secret= client_secret)

    def ready(self):
        import mBlogApp.signals
