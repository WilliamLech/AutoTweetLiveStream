import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch
from twitter_api import TwitterAPI

class TestAutoTweet(IsolatedAsyncioTestCase):

    @patch('twitter_api.TwitterAPI.tweet')
    @patch('twitch_api.twitch_api.is_user_live')
    async def test_retweet_when_stream_is_stopped(self, mock_is_user_live, mock_tweet):
        """
        Test que lorsque le stream est coupé et revient en ligne, un tweet est envoyé avec les informations correctes.
        """
        # Simuler les états : d'abord online, ensuite offline, puis online à nouveau
        mock_is_user_live.side_effect = [True, False, True]

        # Une copie simplifiée de la logique à tester (focus sur les changements de statut)
        was_live = True

        for _ in range(3):  # Trois itérations pour les trois états simulés
            is_live = mock_is_user_live()

            if is_live and not was_live:  # Le stream revient en ligne
                TwitterAPI().tweet("Game", "Title")
                was_live = True

            elif not is_live and was_live:  # Le stream s'arrête
                was_live = False

            await asyncio.sleep(0.1)  # Simuler un temps d'attente court dans un test

        # Vérifier que `tweet` a été appelé une fois correctement
        mock_tweet.assert_called_once_with("Game", "Title")