import json

import jsonpickle
import requests
import time
import params as param

class TwitchAPI:
    def __init__(self):
        self.token = None
        self.expiry = 0

    def _get_app_token(self):
        if self.token and self.expiry > time.time():
            return self.token

        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": param.ID_CLIENT,
            "client_secret": param.SECRET,
            "grant_type": "client_credentials"
        }
        res = requests.post(url, params=params).json()
        self.token = res["access_token"]
        self.expiry = time.time() + res["expires_in"]
        return self.token

    def _get_headers(self):
        return {
            "Client-ID": param.ID_CLIENT,
            "Authorization": f"Bearer {self._get_app_token()}"
        }

    def get_user_id(self, username):
        url = f"https://api.twitch.tv/helix/users?login={username}"
        res = requests.get(url, headers=self._get_headers()).json()
        if "data" in res and len(res["data"]) > 0:
            return res["data"][0]["id"]
        return None

    def is_user_live(self, username):
        user_id = self.get_user_id(username)
        if not user_id:
            return None
        url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
        res = requests.get(url, headers=self._get_headers()).json()
        return res["data"][0] if "data" in res and res["data"] else None



# 👇 Instance prête à être utilisée
twitch_api = TwitchAPI()
