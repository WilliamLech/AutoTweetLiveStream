import requests
from requests_oauthlib import OAuth1

import params

class TwitterAPI:

    def __init__(self):
        self.auth = OAuth1(
            params.TWITTER_API_KEY,
            params.TWITTER_API_SECRET_KEY,
            params.TWITTER_ACCES_TOKEN,
            params.TWITTER_ACCES_SECRET_TOKEN
        )

    def tweet(self,categorie, titreStream):
        str = "Je viens de lancer un stream  \" " + titreStream + " \" sur le jeu " + categorie + " rejoins nous ! https://www.twitch.tv/l3chat_"
        payload= {
            "text": str,
            "for_super_followers_only": False
        }

        response = requests.post(params.TWITTER_API_URL, json = payload,auth=self.auth)
        print(response.text)

twitter_api = TwitterAPI()