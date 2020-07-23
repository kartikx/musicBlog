import requests
import base64
import datetime
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

