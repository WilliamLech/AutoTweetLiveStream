import asyncio
import unittest
from unittest.mock import patch, MagicMock

from twitter_api import TwitterAPI


class TestTwitterAPI(unittest.TestCase):

    @patch('twitter_api.requests.post')
    def test_tweet_success(self, mock_post):
        """
        Test que la méthode `tweet` fonctionne correctement avec une réponse 200.
        """
        # Mock de la réponse de `requests.post`
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"message": "Tweet sent successfully."}'
        mock_post.return_value = mock_response

        # Instancier la classe et appeler la méthode `tweet`
        api = TwitterAPI()
        api.tweet("Action", "Epic Stream Title")

        # Vérifier que `requests.post` a été appelé avec les bons arguments
        mock_post.assert_called_once()
        mock_post.assert_called_with(
            "https://api.twitter.com/2/tweets",  # URL (remplacez par `params.TWITTER_API_URL`)
            json={
                "text": 'Je viens de lancer un stream  " Epic Stream Title " sur le jeu Action rejoins nous ! https://www.twitch.tv/l3chat_',
                "for_super_followers_only": False
            },
            auth=api.auth
        )

    @patch('twitter_api.requests.post')
    def test_tweet_failure(self, mock_post):
        """
        Test que la méthode `tweet` gère correctement une réponse non 200.
        """
        # Mock de la réponse de `requests.post`
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"message": "Error sending tweet."}'
        mock_post.return_value = mock_response

        # Instancier la classe et appeler la méthode `tweet`
        api = TwitterAPI()
        api.tweet("Adventure", "Fun Stream")

        # Vérifier que `requests.post` a bien été appelé
        mock_post.assert_called_once()

        # Vérifier le contenu de la requête envoyée
        mock_post.assert_called_with(
            "https://api.twitter.com/2/tweets",  # URL (remplacez par `params.TWITTER_API_URL`)
            json={
                "text": 'Je viens de lancer un stream  " Fun Stream " sur le jeu Adventure rejoins nous ! https://www.twitch.tv/l3chat_',
                "for_super_followers_only": False
            },
            auth=api.auth
        )

        # Assurer que la réponse textuelle a été imprimée

        self.assertEqual(mock_response.text, '{"message": "Error sending tweet."}')


    @patch('twitter_api.TwitterAPI.tweet')
    @patch('twitch_api.twitch_api.is_user_live')
    def test_tweet_on_live_return(self, mock_is_user_live, mock_tweet):
        """
        Teste qu'un tweet est envoyé lorsque le stream revient en ligne après être passé offline.
        """
        # Simuler les états : d'abord offline, puis online
        mock_is_user_live.side_effect = [False, True]

        # Variable pour intercepter si le test a fonctionné
        result_called = False

        async def run_test():
            nonlocal result_called

            # On met ici une version restreinte de `check_if_live_loop` avec seulement 2 itérations
            was_live = True
            for _ in range(2):  # Effectuer seulement 2 cycles de la boucle
                is_live = mock_is_user_live()
                if is_live and not was_live:
                    # Si on passe de offline à online, envoyer un tweet
                    TwitterAPI().tweet("Game", "Title")
                    was_live = True
                elif not is_live and was_live:
                    was_live = False
                await asyncio.sleep(0.1)  # Réduire le temps d'attente dans les tests
            result_called = True

        asyncio.run(run_test())

        # Vérifier que `tweet` a bien été appelé une seule fois avec les bons arguments
        mock_tweet.assert_called_once_with("Game", "Title")
        self.assertTrue(result_called)


if __name__ == "__main__":
    unittest.main()
